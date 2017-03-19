# coding=utf-8
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from feira.tests_modules.helpers import post_as_json, put_as_json, get_response_content
from feira.tests_data.feiras_data import test_data as feiras_test_data
from feira.tests_data.feira_data import test_data


class FeiraTestes(TestCase):
    """Testes do endpoint /feira/<id>/"""

    def settings(self, **kwargs):
        self.client = Client()

    def test_metodo_nao_permitido(self):
        u"""Tenta executar um método não permitido"""
        response = self.client.post(reverse("api-feira-id", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 405, "Deve retornar status 405")

    def test_get_nao_encontrado(self):
        response = self.client.get(reverse("api-feira-id", kwargs={"id": 99999}))
        self.assertEqual(response.status_code, 404, "Deve retornar status 404")

    def test_get_id(self):
        u"""Adiciona três feiras e tenta recuperar uma delas"""
        post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id"])
        post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id_2"])
        post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id_3"])

        response = self.client.get(reverse("api-feira-id", kwargs={"id": 2}))
        content = get_response_content(response)
        nome_2 = feiras_test_data["com_id_2"]["nome"]
        self.assertEqual(response.status_code, 200, "Deve retornar status 200")
        self.assertEqual(content["results"][0]["nome"], nome_2, u"Deve retonrnar a feira com nome = {}".format(nome_2))

    def test_delete(self):
        u"""Adiciona uma feira, exclui em seguida e verifica se foi mesmo excluída"""
        id = feiras_test_data["com_id_2"]["id"]
        post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id_2"])
        response = self.client.delete(reverse("api-feira-id", kwargs={"id": id}))
        content = get_response_content(response)
        self.assertEqual(response.status_code, 200, "Deve retornar status 200")
        self.assertEqual(
            content["message"],
            u"Feira {} removida com sucesso".format(id),
            u"Deve retornar mensagem de confirmação de feira excluida"
        )

        response = self.client.get(reverse("api-feira-id", kwargs={"id": id}))
        self.assertEqual(response.status_code, 404, "Deve retornar status 404")

    def test_put(self):
        u"""Adiciona uma feira e altera o nome"""
        response = post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id_2"])
        content = get_response_content(response)
        id = content["results"][0]["id"]
        nome_anterior = content["results"][0]["nome"]
        nome_novo = nome_anterior + " NOVO"
        put_data = {"nome": nome_novo}

        response = put_as_json(self.client, reverse("api-feira-id", kwargs={"id": id}), put_data)
        content = get_response_content(response)
        self.assertEqual(response.status_code, 200, u"Deve retornar status 200")
        self.assertEqual(content["results"][0]["nome"], nome_novo, u"Deve mudar o nome para {}".format(nome_novo))
        self.assertNotEqual(content["results"][0]["nome"], nome_anterior, u"Nome novo deve ser diferente do anterior")

    def test_put_invalido(self):
        u"""Tenta alterar o ID da feira"""
        response = post_as_json(self.client, reverse("api-feiras"), feiras_test_data["com_id_2"])
        content = get_response_content(response)
        id = content["results"][0]["id"]
        id_novo = id + 1
        put_data = {"id": id_novo}

        response = put_as_json(self.client, reverse("api-feira-id", kwargs={"id": id}), put_data)
        content = get_response_content(response)
        self.assertEqual(response.status_code, 500, u"Deve retornar status 500")
        self.assertEqual(
            content["message"],
            u"Campo id não pode ser alterado: {} => {}".format(id, id_novo),
            u"Deve retornar mensagem de erro"
        )
