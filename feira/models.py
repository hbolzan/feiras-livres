# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Distrito(models.Model):
    codigo = models.IntegerField(u"Código", primary_key=True, help_text="Código do Distrito Municipal conforme IBGE")
    nome = models.CharField(u"Nome", max_length=18, help_text="Nome do Distrito Municipal")

    def __unicode__(self):
        return self.nome


class Subprefeitura(models.Model):
    codigo = models.IntegerField(u"Código", primary_key=True,
                                 help_text="Código de cada uma das 31 Subprefeituras (2003 a 2012)")
    nome = models.CharField(u"Nome", max_length=25, help_text="Nome da Subprefeitura (31 de 2003 até 2012)")

    def __unicode__(self):
        return self.nome


class Feira(models.Model):
    longitude = models.CharField(
        u"Longitude",
        max_length=10,
        help_text="Longitude da localização do estabelecimento no território do Município"
    )
    latitude = models.CharField(
        u"Latitude",
        max_length=10,
        help_text="Latitude da localização do estabelecimento no território do Município"
    )
    setor_censitario = models.CharField(
        u"Setor censitário",
        max_length=15,
        help_text="Setor censitário conforme IBGE")
    area_ponderacao = models.CharField(
        u"Área de ponderação",
        max_length=13,
        help_text="Área de ponderação (agrupamento de setores censitários) conforme IBGE 2010")
    distrito = models.ForeignKey(Distrito, verbose_name=u"Distrito")
    subprefeitura = models.ForeignKey(Subprefeitura, verbose_name=u"Subprefeitura")
    regiao_5 = models.CharField(u"Região 5", max_length=6, help_text=u"Região conforme divisão do Município em 5 áreas")
    regiao_8 = models.CharField(u"Região 8", max_length=7, help_text=u"Região conforme divisão do Município em 8 áreas")
    nome = models.CharField(
        u"Nome da feira livre",
        max_length=30,
        help_text=u"Denominação da feira livre atribuída pela Supervisão de Abastecimento"
    )
    registro = models.CharField(u"Registro", max_length=6, help_text="Número do registro da feira livre na PMSP")
    logradouro = models.CharField(
        u"Logradouro",
        max_length=34,
        help_text=u"Nome do logradouro onde se localiza a feira livre"
    )
    numero = models.CharField(
        u"Número",
        max_length=5,
        help_text=u"Um número do logradouro onde se localiza a feira livre"
    )
    bairro = models.CharField(u"Bairro", max_length=20, help_text=u"Bairro de localização da feira livre")
    referencia = models.CharField(
        u"Ponto de referência",
        max_length=24,
        help_text=u"Ponto de referência da localização da feira livre"
    )
