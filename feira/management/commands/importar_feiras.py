#-*- coding:utf-8 -*-
from __future__ import print_function
import csv
from django.core.management.base import BaseCommand
from argparse import RawTextHelpFormatter
from feira.models import Distrito, Subprefeitura, Feira


class Command(BaseCommand):
    help = u"Importação não incremental do arquivo CSV de feiras livres da prefeitura de São Paulo\n\n" \
           u"Modo de uso:\n" \
           u"  ./manage.py importar_feiras /caminho/para/o/arquivo.csv"

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument('csv', type=str)

    def handle(self, *args, **options):
        csv_path = options["csv"]
        try:
            with open(csv_path) as csvfile:
                limpar_tabelas()
                reader = csv.DictReader(csvfile)
                for linha in reader:
                    feira = adicionar_linha(linha)
                    print(feira.id, feira.nome)
        except IOError:
            print(u"\nERRO\nArquivo {} não existe\n".format(csv))


def limpar_tabelas():
    Feira.objects.all().delete()
    Distrito.objects.all().delete()
    Subprefeitura.objects.all().delete()


def adicionar_linha(linha):
    distrito, created = Distrito.objects.get_or_create(codigo=linha["CODDIST"], nome=linha["DISTRITO"])
    subprefeitura, created = Subprefeitura.objects.get_or_create(codigo=linha["CODSUBPREF"], nome=linha["SUBPREFE"])
    return Feira.objects.create(
        id=int(linha["ID"]),
        longitude=linha["LONG"],
        latitude=linha["LAT"],
        setor_censitario=linha["SETCENS"],
        area_ponderacao=linha["AREAP"],
        distrito=distrito,
        subprefeitura=subprefeitura,
        regiao_5=linha["REGIAO5"],
        regiao_8=linha["REGIAO8"],
        nome=linha["NOME_FEIRA"],
        registro=linha["REGISTRO"],
        logradouro=linha["LOGRADOURO"],
        numero=linha["NUMERO"],
        bairro=linha["BAIRRO"],
        referencia=linha["REFERENCIA"]
    )
