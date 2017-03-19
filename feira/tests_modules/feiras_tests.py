# coding=utf-8
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from feira.tests_modules.helpers import post_as_json, get_response_content
from feira.tests_data.feiras_data import test_data

# Create your tests here.


class FeirasTestes(TestCase):
    """Testes do endpoint /feiras/"""

    def settings(self, **kwargs):
        self.client = Client()

    def test_metodo_nao_permitido(self):
        u"""Tenta executar um método não permitido"""
        response = self.client.put(reverse("api-feiras"))
        self.assertEqual(response.status_code, 405, "Deve retornar status 405")

    def test_post_com_id(self):
        """Adiciona uma feira informando o ID"""
        response = post_as_json(self.client, reverse("api-feiras"), test_data["com_id"])
        self.assertEqual(response.status_code, 200, "Deve adicionar uma feira e retornar status 200")

    def test_post_sem_id(self):
        """Adiciona uma feira sem informar o id"""
        response = post_as_json(self.client, reverse("api-feiras"), test_data["sem_id"])
        content = get_response_content(response)
        self.assertEqual(content["results"][0]["id"], 1, "Deve adicionar uma feira com código 1")

    def test_post_com_id_repetido(self):
        """Adiciona uma feira informando um ID repetido"""
        post_as_json(self.client, reverse("api-feiras"), test_data["com_id"])
        response = post_as_json(self.client, reverse("api-feiras"), test_data["com_id"])
        content = get_response_content(response)
        self.assertEqual(response.status_code, 500, "Deve retornar status 500")
        self.assertEqual(
            content.get("message"),
            u"O id informado já existe no cadastro de feiras",
            u"Deve retornar uma mensagem informando que o id já está cadastrado"
        )

    def test_post_faltando_campo_obrigatorio(self):
        u"""Adiciona uma feira faltando um campo obrigatório"""
        response = post_as_json(self.client, reverse("api-feiras"), test_data["faltando_campos"])
        self.assertEqual(response.status_code, 500, "Deve gerar erro 500")
        self.assertEqual(
            get_response_content(response).get("message"),
            u"Os seguintes campos obrigatórios não foram preenchidos: longitude",
            u"Deve retornar uma mensagem de erro com a lista de campos obrigatórios não preenchidos"
        )

    def test_post_campo_relacionado_invalido(self):
        """Adiciona uma com um distrito inexistente sem informar nome para adicionar na tabela relacionada"""
        response = post_as_json(self.client, reverse("api-feiras"), test_data["distrito_invalido"])
        content = get_response_content(response)
        self.assertEqual(response.status_code, 500, "Deve retornar status 500")
        self.assertEqual(
            content.get("message"),
            u"O código informado para distrito não existe",
            u"Deve retornar uma mensagem informando que o código de distrito é inválido"
        )

    def test_list(self):
        """Recupera todas as feiras cadastradas"""
        # adiciona 4 feiras
        url = reverse("api-feiras")
        post_as_json(self.client, url, test_data["sem_id"])
        post_as_json(self.client, url, test_data["sem_id"])
        post_as_json(self.client, url, test_data["sem_id"])
        post_as_json(self.client, url, test_data["sem_id"])

        response = self.client.get(url)
        content = get_response_content(response)
        self.assertEqual(response.status_code, 200, "Deve retornar status 200")
        self.assertEqual(content["count"], 4, "Deve retornar contagem igual 4")
        self.assertEqual(len(content["results"]), 4, "Deve retornar 4 feiras")
