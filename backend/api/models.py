from django.db import models
from rest_framework.permissions import IsAuthenticated


class Parada(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Latitude = models.FloatField()
    Longitude = models.FloatField()

    def __str__(self):
        text = f"""Name: {self.Name}, Latitude: {self.Latitude},
                Longitude: {self.Longitude}"""
        return text


class Linha(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Paradas = models.ManyToManyField(Parada)

    def __str__(self):
        text = f"Name: {self.Name}, Paradas: {self.Paradas}"
        return text


class Veiculo(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=200)
    Modelo = models.CharField(max_length=200)
    LinhaId = models.ForeignKey(
        Linha,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        text = f"""Name: {self.Name}, Modelo: {self.Modelo},
                LinhaId: {self.LinhaId}"""
        return text


class PosicaoVeiculo(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    VeiculoId = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    def __str__(self):
        text = f"""Veiculo: {self.VeiculoId}, Latitude: {self.Latitude},
                Longitude: {self.Longitude}"""
        return text
