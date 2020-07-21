from .models import Parada, Linha, Veiculo, PosicaoVeiculo
from rest_framework import serializers


class ParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parada
        fields = ['Id', 'Name', 'Latitude', 'Longitude']


class LinhaSerializer(serializers.ModelSerializer):
    Paradas = serializers.PrimaryKeyRelatedField(many=True, queryset=Parada.objects.all())

    class Meta:
        model = Linha
        fields = ['Id', 'Name', 'Paradas']


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['Id', 'Name', 'Modelo', 'LinhaId']


class PosicaoVeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicaoVeiculo
        fields = ['VeiculoId', 'Latitude', 'Longitude']


class DistanciaParadaSerializer(serializers.Serializer):
    distancia = serializers.FloatField()
    Parada = ParadaSerializer(read_only=True)
