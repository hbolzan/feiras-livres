# coding=utf-8
from django.test import TestCase, Client
from django.urls import reverse
from feira.tests_modules.helpers import post_as_json, get_response_content
from feira.tests_data.feiras_busca_data import test_data
from feira.views import MENSAGEM_BUSCA_INVALIDA


class FeirasBuscaTestes(TestCase):
    """Testes do endpoint /feiras/busca/"""
    def settings(self, **kwargs):
        self.client = Client()

    def AdicionarFeiras(self):
        url = reverse("api-feiras")
        for feira in test_data["feiras"]:
            response = post_as_json(self.client, url, feira)
            self.assertEqual(response.status_code, 200, u"POST Deve retornar status 200")

    def test_busca_invalida(self):
        """Tenta fazer uma busca com parâmetros não preenchidos"""
        response = self.client.get(reverse("api-feiras-busca"))
        content = get_response_content(response)
        self.assertEqual(response.status_code, 500, u"Deve retornar status 500")
        self.assertEqual(content["message"], MENSAGEM_BUSCA_INVALIDA, u"Deve retornar mensagem de erro")

    def test_busca(self):
        """Adiciona feiras e faz uma busca simples por nome"""
        self.AdicionarFeiras()
        for nome, queries in test_data["queries"].iteritems():
            for query in queries:
                response = self.client.get(reverse("api-feiras-busca"), query["params"])
                content = get_response_content(response)
                self.assertEqual(response.status_code, 200, u"Deve retornar status 200")
                self.assertEqual(
                    content["count"],
                    query["results_count"],
                    u"Deve retornar a quantidade esperada de feiras"
                )
