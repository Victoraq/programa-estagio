import json
from rest_framework import status
from django.test import TestCase, Client

from .utils import coords_distance
from .models import Parada, Linha, Veiculo, PosicaoVeiculo
from .serializers import (
    ParadaSerializer,
    LinhaSerializer,
    VeiculoSerializer,
    PosicaoVeiculoSerializer
)

# initialize the APIClient app
client = Client()


class BaseAPITestCase(TestCase):
    def setUp(self):
        # Inicializa as paradas
        self.rio_branco = Parada.objects.create(
            Name="Rio Branco",
            Latitude="-21.765289",
            Longitude="-43.348638"
        )
        self.catedral = Parada.objects.create(
            Name="Catedral",
            Latitude="-21.764055",
            Longitude="-43.348963"
        )
        self.stella = Parada.objects.create(
            Name="Stella",
            Latitude="-21.765500",
            Longitude="-43.347676"
        )

        # Inicializa as linhas
        self.linha1 = Linha.objects.create(Name="Linha 1")
        self.linha2 = Linha.objects.create(Name="Linha 2")

        self.linha1.Paradas.add(self.rio_branco.Id)
        self.linha1.Paradas.add(self.catedral.Id)
        self.linha1.Paradas.add(self.stella.Id)
        self.linha2.Paradas.add(self.stella.Id)
        self.linha2.Paradas.add(self.rio_branco.Id)

        # Inicializa os veiculos
        self.veiculo1 = Veiculo.objects.create(
            Name="veiculo1",
            Modelo="CCXP",
            LinhaId=self.linha1
        )
        self.veiculo2 = Veiculo.objects.create(
            Name="veiculo2",
            Modelo="CCXP",
            LinhaId=self.linha1
        )
        self.veiculo3 = Veiculo.objects.create(
            Name="veiculo3",
            Modelo="CCXPX",
            LinhaId=self.linha2
        )

        # Posicao de cada veiculo
        self.pos_v1 = PosicaoVeiculo.objects.create(
            Latitude=self.rio_branco.Latitude,
            Longitude=self.rio_branco.Longitude,
            VeiculoId=self.veiculo1
        )
        self.pos_v2 = PosicaoVeiculo.objects.create(
            Latitude=self.catedral.Latitude,
            Longitude=self.catedral.Longitude,
            VeiculoId=self.veiculo2
        )
        self.pos_v3 = PosicaoVeiculo.objects.create(
            Latitude=self.stella.Latitude,
            Longitude=self.stella.Longitude,
            VeiculoId=self.veiculo3
        )

        # Novos JSONs

        # Paradas
        self.valid_parada = {
            "Name": "Colegio",
            "Latitude": "-21.768120",
            "Longitude": "-43.350203"
        }

        self.invalid_parada = {
            "Name": "",
            "Latitude": "-21.768120",
            "Longitude": "-43.350203"
        }

        # Linhas
        self.valid_linha = {
            "Name": "Linha Valida",
            "Paradas": [self.rio_branco.Id, self.stella.Id]
        }

        self.invalid_linha = {
            "Name": "",
            "Paradas": [self.rio_branco.Id, self.stella.Id]
        }

        # Veiculos
        self.valid_veiculo = {
            "Name": "VeiculoNovo",
            "Modelo": "MM95",
            "LinhaId": self.linha2.Id
        }

        self.invalid_veiculo = {
            "Name": "",
            "Modelo": "WW96",
            "LinhaId": 53213
        }

        # Posicao Veiculo
        self.valid_posicao_veiculo = {
            "Latitude": "-21.765289",
            "Longitude": "-43.348638",
            "VeiculoId": self.veiculo2.Id
        }

        self.invalid_posicao_veiculo = {
            "Latitude": "-21.765289",
            "Longitude": "-43.348638",
            "VeiculoId": 27321
        }


class ParadaTest(BaseAPITestCase):
    """
    Modulo de testes para endpoint de Parada.
    """

    def test_get_all_paradas(self):
        # get API response
        response = client.get('/parada')
        # get paradas from db
        paradas = Parada.objects.all()
        serializer = ParadaSerializer(paradas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_parada(self):
        # get API response after post
        response = client.post(
            '/parada',
            data=json.dumps(self.valid_parada),
            content_type='application/json'
        )
        # get paradas from db
        paradas = Parada.objects.all()
        serializer = ParadaSerializer(paradas, many=True)
        self.assertIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_parada(self):
        # get API response after post
        response = client.post(
            '/parada',
            data=json.dumps(self.invalid_parada),
            content_type='application/json'
        )
        # get paradas from db
        paradas = Parada.objects.all()
        serializer = ParadaSerializer(paradas, many=True)
        self.assertNotIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_parada_by_id(self):
        # get API response from an already insert instance
        response = client.get(f'/parada/{self.rio_branco.Id}')
        serializer = ParadaSerializer(self.rio_branco)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_linhas_by_parada_id(self):
        # get API response from an already insert instance
        response = client.get(f'/parada/linhasPorParada/{self.rio_branco.Id}')
        # serializando linhas que contem a parada
        serializer = LinhaSerializer([self.linha1, self.linha2], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_paradas_por_posicao(self):

        lat, long = (-21.766282, -43.348492)

        # resposta ta api das paradas proximas ao ponto
        response = client.get(
            f'/parada/paradasPorPosicao/?lat={lat}&long={long}'
        )

        # get paradas from db
        paradas = Parada.objects.all()
        serializer = ParadaSerializer(paradas, many=True)

        response_distances = list(map(lambda x: x['distancia'], response.data))
        calculated_distances = list(map(
            lambda x: coords_distance(
                    float(lat), float(long), x["Latitude"], x["Longitude"]
                ),
            serializer.data
            ))
        calculated_distances.sort()

        self.assertEqual(response_distances, calculated_distances)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_parada_by_id(self):
        # get API response from a invalid Id
        response = client.get('/parada/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_parada_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/parada/{self.rio_branco.Id}',
            data=json.dumps(self.valid_parada),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_parada_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/parada/{self.rio_branco.Id}',
            data=json.dumps(self.invalid_parada),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_parada_by_invalid_id(self):
        # get API response from update instance
        response = client.put(
            '/parada/30',
            data=json.dumps(self.valid_parada),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_parada(self):
        response = client.delete(f'/parada/{self.rio_branco.Id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_parada(self):
        response = client.delete('/parada/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LinhaTest(BaseAPITestCase):
    """
    Modulo de testes para endpoint de Linha.
    """

    def test_get_all_linhas(self):
        # get API response
        response = client.get('/linha')
        # get linhas from db
        linhas = Linha.objects.all()
        serializer = LinhaSerializer(linhas, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_linha(self):
        # get API response after post
        response = client.post(
            '/linha',
            data=json.dumps(self.valid_linha),
            content_type='application/json'
        )
        # get linhas from db
        linhas = Linha.objects.all()
        serializer = LinhaSerializer(linhas, many=True)
        self.assertIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_linha(self):
        # get API response after post
        response = client.post(
            '/linha',
            data=json.dumps(self.invalid_linha),
            content_type='application/json'
        )
        # get linhas from db
        linhas = Linha.objects.all()
        serializer = LinhaSerializer(linhas, many=True)
        self.assertNotIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_linha_by_id(self):
        # get API response from an already insert instance
        response = client.get(f'/linha/{self.linha1.Id}')
        serializer = LinhaSerializer(self.linha1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_linha_by_id(self):
        # get API response from a invalid Id
        response = client.get('/linha/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_veculos_by_linha_id(self):
        # get API response from an already insert instance
        response = client.get(f'/linha/veiculosPorLinha/{self.linha1.Id}')
        # serializando veiculos que passam na linha
        serializer = LinhaSerializer([self.veiculo1, self.veiculo2], many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_valid_linha_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/linha/{self.linha1.Id}',
            data=json.dumps(self.valid_linha),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_linha_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/linha/{self.linha1.Id}',
            data=json.dumps(self.invalid_linha),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_linha_by_invalid_id(self):
        # get API response from update instance
        response = client.put(
            '/linha/30',
            data=json.dumps(self.valid_linha),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_linha(self):
        response = client.delete(f'/linha/{self.linha1.Id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_linha(self):
        response = client.delete('/linha/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VeiculoTest(BaseAPITestCase):
    """
    Modulo de testes para endpoint de Veiculo.
    """

    def test_get_all_veiculos(self):
        # get API response
        response = client.get('/veiculo')
        # get veiculos from db
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_veiculo(self):
        # get API response after post
        response = client.post(
            '/veiculo',
            data=json.dumps(self.valid_veiculo),
            content_type='application/json'
        )
        # get veiculos from db
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos, many=True)
        self.assertIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_veiculo(self):
        # get API response after post
        response = client.post(
            '/veiculo',
            data=json.dumps(self.invalid_veiculo),
            content_type='application/json'
        )
        # get veiculos from db
        veiculos = Veiculo.objects.all()
        serializer = VeiculoSerializer(veiculos, many=True)
        self.assertNotIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_veiculo_by_id(self):
        # get API response from an already insert instance
        response = client.get(f'/veiculo/{self.veiculo1.Id}')
        serializer = VeiculoSerializer(self.veiculo1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_veiculo_by_id(self):
        # get API response from a invalid Id
        response = client.get('/veiculo/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_veiculo_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/veiculo/{self.veiculo1.Id}',
            data=json.dumps(self.valid_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_veiculo_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/veiculo/{self.veiculo1.Id}',
            data=json.dumps(self.invalid_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_veiculo_by_invalid_id(self):
        # get API response from update instance
        response = client.put(
            '/veiculo/30',
            data=json.dumps(self.valid_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_veiculo(self):
        response = client.delete(f'/veiculo/{self.veiculo1.Id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_veiculo(self):
        response = client.delete('/veiculo/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PosicaoVeiculoTest(BaseAPITestCase):
    """
    Modulo de testes para endpoint de PosicaoVeiculo.
    """

    def test_get_all_posicoes(self):
        # get API response
        response = client.get('/posicaoVeiculo')
        # get posicoes from db
        posicoes = PosicaoVeiculo.objects.all()
        serializer = PosicaoVeiculoSerializer(posicoes, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_posicao_veiculo(self):
        # get API response after post
        response = client.post(
            '/posicaoVeiculo',
            data=json.dumps(self.valid_posicao_veiculo),
            content_type='application/json'
        )
        # get posicoes from db
        posicoes = PosicaoVeiculo.objects.all()
        serializer = PosicaoVeiculoSerializer(posicoes, many=True)
        self.assertIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_posicao_veiculo(self):
        # get API response after post
        response = client.post(
            '/posicaoVeiculo',
            data=json.dumps(self.invalid_posicao_veiculo),
            content_type='application/json'
        )
        # get posicoes from db
        posicoes = PosicaoVeiculo.objects.all()
        serializer = PosicaoVeiculoSerializer(posicoes, many=True)
        self.assertNotIn(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_posicao_veiculo_by_id(self):
        # get API response from an already insert instance
        response = client.get(f'/posicaoVeiculo/{self.pos_v1.Id}')
        serializer = PosicaoVeiculoSerializer(self.pos_v1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_posicao_veiculo_by_id(self):
        # get API response from a invalid Id
        response = client.get('/posicaoVeiculo/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_posicao_veiculo_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/posicaoVeiculo/{self.pos_v1.Id}',
            data=json.dumps(self.valid_posicao_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid_posicao_veiculo_by_id(self):
        # get API response from update instance
        response = client.put(
            f'/posicaoVeiculo/{self.pos_v1.Id}',
            data=json.dumps(self.invalid_posicao_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_posicao_veiculo_by_invalid_id(self):
        # get API response from update instance
        response = client.put(
            '/posicaoVeiculo/30',
            data=json.dumps(self.valid_posicao_veiculo),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_valid_posicao_veiculo(self):
        response = client.delete(f'/posicaoVeiculo/{self.pos_v1.Id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_posicao_veiculo(self):
        response = client.delete('/posicaoVeiculo/30')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
