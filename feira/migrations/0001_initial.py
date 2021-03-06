# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-19 19:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('codigo', models.IntegerField(help_text='C\xf3digo do Distrito Municipal conforme IBGE', primary_key=True, serialize=False, verbose_name='C\xf3digo')),
                ('nome', models.CharField(help_text='Nome do Distrito Municipal', max_length=18, verbose_name='Nome')),
            ],
        ),
        migrations.CreateModel(
            name='Feira',
            fields=[
                ('id', models.AutoField(help_text='N\xfamero de identifica\xe7\xe3o do estabelecimento georreferenciado por SMDU/Deinfo', primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.CharField(help_text='Longitude da localiza\xe7\xe3o do estabelecimento no territ\xf3rio do Munic\xedpio', max_length=10, verbose_name='Longitude')),
                ('latitude', models.CharField(help_text='Latitude da localiza\xe7\xe3o do estabelecimento no territ\xf3rio do Munic\xedpio', max_length=10, verbose_name='Latitude')),
                ('setor_censitario', models.CharField(help_text='Setor censit\xe1rio conforme IBGE', max_length=15, verbose_name='Setor censit\xe1rio')),
                ('area_ponderacao', models.CharField(help_text='\xc1rea de pondera\xe7\xe3o (agrupamento de setores censit\xe1rios) conforme IBGE 2010', max_length=13, verbose_name='\xc1rea de pondera\xe7\xe3o')),
                ('regiao_5', models.CharField(help_text='Regi\xe3o conforme divis\xe3o do Munic\xedpio em 5 \xe1reas', max_length=6, verbose_name='Regi\xe3o 5')),
                ('regiao_8', models.CharField(help_text='Regi\xe3o conforme divis\xe3o do Munic\xedpio em 8 \xe1reas', max_length=7, verbose_name='Regi\xe3o 8')),
                ('nome', models.CharField(help_text='Denomina\xe7\xe3o da feira livre atribu\xedda pela Supervis\xe3o de Abastecimento', max_length=30, verbose_name='Nome da feira livre')),
                ('registro', models.CharField(help_text='N\xfamero do registro da feira livre na PMSP', max_length=6, verbose_name='Registro')),
                ('logradouro', models.CharField(help_text='Nome do logradouro onde se localiza a feira livre', max_length=34, verbose_name='Logradouro')),
                ('numero', models.CharField(help_text='Um n\xfamero do logradouro onde se localiza a feira livre', max_length=5, verbose_name='N\xfamero')),
                ('bairro', models.CharField(help_text='Bairro de localiza\xe7\xe3o da feira livre', max_length=20, verbose_name='Bairro')),
                ('referencia', models.CharField(blank=True, help_text='Ponto de refer\xeancia da localiza\xe7\xe3o da feira livre', max_length=24, null=True, verbose_name='Ponto de refer\xeancia')),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feira.Distrito', verbose_name='Distrito')),
            ],
        ),
        migrations.CreateModel(
            name='Subprefeitura',
            fields=[
                ('codigo', models.IntegerField(help_text='C\xf3digo de cada uma das 31 Subprefeituras (2003 a 2012)', primary_key=True, serialize=False, verbose_name='C\xf3digo')),
                ('nome', models.CharField(help_text='Nome da Subprefeitura (31 de 2003 at\xe9 2012)', max_length=25, verbose_name='Nome')),
            ],
        ),
        migrations.AddField(
            model_name='feira',
            name='subprefeitura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feira.Subprefeitura', verbose_name='Subprefeitura'),
        ),
    ]
