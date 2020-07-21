from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404

from .utils import coords_distance
from .models import Parada, Linha, Veiculo, PosicaoVeiculo
from .serializers import (
    ParadaSerializer,
    DistanciaParadaSerializer,
    LinhaSerializer,
    VeiculoSerializer,
    PosicaoVeiculoSerializer
)


class ParadaList(APIView):
    """
    get:
    Retorna uma lista de todas as Paradas existentes.

    post:
    Cria uma nova instância de Parada.
    """
    def get(self, request, pk=None, format=None):
        paradas = get_list_or_404(Parada)
        serializer = ParadaSerializer(paradas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ParadaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParadaDetail(APIView):
    """
    get:
    Retorna a instância de Parada indentificada pelo parâmetro.

    post:
    Modifica a instância de Parada indentificada pelo parâmetro.

    delete:
    Deleta a instância de Parada indentificada pelo parâmetro.
    """
    def get(self, request, pk=None, format=None):
        parada = get_object_or_404(Parada, pk=pk)
        serializer = ParadaSerializer(parada)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        parada = get_object_or_404(Parada, pk=pk)
        serializer = ParadaSerializer(parada, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        parada = get_object_or_404(Parada, pk=pk)
        parada.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def linhas_por_parada(request, pk=None, format=None):
    """
    Recebe o identificador de uma parada e retorna as linhas associadas
    a parada informada.
    """
    parada = get_object_or_404(Parada, pk=pk)
    linhas = parada.linha_set.all()
    serializer = LinhaSerializer(linhas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def paradas_por_posicao(request, format=None):
    """
    Retorna lista paradas mais próximas do ponto passado por parâmetro.

    parameters:
    lat - Latitude
    long - Longitude

    Exemplo: lat=42.213&long=-31.231

    Obs: Distância em Kilometros
    """
    lat = request.GET.get('lat', '')
    long = request.GET.get('long', '')

    if lat == '' or long == '':
        return Response(status=status.HTTP_400_BAD_REQUEST)

    paradas = get_list_or_404(Parada)
    serializer = ParadaSerializer(paradas, many=True)

    # map sobre a lista de paradas para calcular as distancias entre o ponto
    # e as paradas
    dist = map(
        lambda x: {
            'distancia': coords_distance(
                    float(lat), float(long), x["Latitude"], x["Longitude"]
                ),
            'Parada': x
        },
        serializer.data
    )

    # Ordenando pela distancia
    dist = sorted(dist, key=lambda x: x['distancia'])

    serializer = DistanciaParadaSerializer(dist, many=True)

    return Response(serializer.data)


class LinhaList(APIView):
    """
    get:
    Retorna uma lista de todas as Linhas existentes.

    post:
    Cria uma nova instância de Linha.
    """
    def get(self, request, format=None):
        linhas = get_list_or_404(Linha)
        serializer = LinhaSerializer(linhas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LinhaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinhaDetail(APIView):
    """
    get:
    Retorna a instância de Linha indentificada pelo parâmetro.

    post:
    Modifica a instância de Linha indentificada pelo parâmetro.

    delete:
    Deleta a instância de Linha indentificada pelo parâmetro.
    """
    def get(self, request, pk=None, format=None):
        linha = get_object_or_404(Linha, pk=pk)
        serializer = LinhaSerializer(linha)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        linha = get_object_or_404(Linha, pk=pk)
        serializer = LinhaSerializer(linha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        linha = get_object_or_404(Linha, pk=pk)
        linha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def veiculos_por_linha(request, pk=None, format=None):
    """
    Recebe o identificador de uma linha e retorna os veículos associados
    a linha informada.
    """
    linha = get_object_or_404(Linha, pk=pk)
    veiculos = linha.veiculo_set.all()
    serializer = LinhaSerializer(veiculos, many=True)
    return Response(serializer.data)


class VeiculoList(APIView):
    """
    get:
    Retorna uma lista de todos os Veículos existentes.

    post:
    Cria uma nova instância de Veículo.
    """
    def get(self, request, format=None):
        veiculos = get_list_or_404(Veiculo)
        serializer = VeiculoSerializer(veiculos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VeiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VeiculoDetail(APIView):
    """
    get:
    Retorna a instância de Veículo indentificada pelo parâmetro.

    post:
    Modifica a instância de Veículo indentificada pelo parâmetro.

    delete:
    Deleta a instância de Veículo indentificada pelo parâmetro.
    """
    def get(self, request, pk=None, format=None):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        serializer = VeiculoSerializer(veiculo)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        serializer = VeiculoSerializer(veiculo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        veiculo = get_object_or_404(Veiculo, pk=pk)
        veiculo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PosicaoVeiculoList(APIView):
    """
    get:
    Retorna uma lista de todas as Posições de Veículos existentes.

    post:
    Cria uma nova instância de Posição de Veículo.
    """
    def get(self, request, format=None):
        posicao = get_list_or_404(PosicaoVeiculo)
        serializer = PosicaoVeiculoSerializer(posicao, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PosicaoVeiculoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PosicaoVeiculoDetail(APIView):
    """
    get:
    Retorna a instância de Posição de Veículo indentificada pelo parâmetro.

    post:
    Modifica a instância de Posição de Veículo indentificada pelo parâmetro.

    delete:
    Deleta a instância de Posição de Veículo indentificada pelo parâmetro.
    """
    def get(self, request, pk=None, format=None):
        posicao = get_object_or_404(PosicaoVeiculo, pk=pk)
        serializer = PosicaoVeiculoSerializer(posicao)
        return Response(serializer.data)

    def put(self, request, pk=None, format=None):
        posicao = get_object_or_404(PosicaoVeiculo, pk=pk)
        serializer = PosicaoVeiculoSerializer(posicao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        posicao = get_object_or_404(PosicaoVeiculo, pk=pk)
        posicao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
