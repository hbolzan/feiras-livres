# coding=utf-8
import json
import operator

from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from .models import Distrito, Subprefeitura, Feira

# Create your views here.

MENSAGEM_404 = u"O ID solicitado não existe no cadastro de feiras"

CAMPOS_OBRIGATORIOS = [
    f.name + ("_id" if f.is_relation else "") for f in Feira._meta.fields if f.name != "id" and not f.null
]

CAMPOS_BUSCA = {
    "distrito": "distrito__nome",
    "regiao_5": "regiao_5",
    "nome": "nome",
    "bairro": "bairro",
}


class MetodoNaoPermitido(Exception):
    pass


class DadosInvalidos(Exception):
    pass


@csrf_exempt
def feiras(request):
    try:
        validar_metodo(request.method, ["GET", "POST"])
        if request.method == "POST":
            return feira_get_id(request, adicionar_feira(request).id)
        return feira_get(Feira.objects.all())
    except Feira.DoesNotExist:
        return status_response(404, MENSAGEM_404)
    except MetodoNaoPermitido as erro:
        return metodo_nao_permitido(erro)
    except (DadosInvalidos, Exception) as erro:
        return status_response(500, unicode(erro))


@csrf_exempt
def feira(request, id):
    try:
        validar_metodo(request.method, ["GET", "DELETE", "PUT", "PATCH"])
        return metodos[request.method](request, id)
    except Feira.DoesNotExist:
        return status_response(404, MENSAGEM_404)
    except MetodoNaoPermitido as erro:
        return metodo_nao_permitido(erro)
    except (DadosInvalidos, Exception) as erro:
        return status_response(500, unicode(erro))


def feiras_busca(request):
    try:
        validar_metodo(request.method, ["GET"])
        return feiras_filter(request)
    except MetodoNaoPermitido as erro:
        return metodo_nao_permitido(erro)
    except (DadosInvalidos, Exception) as erro:
        return status_response(500, unicode(erro))


def feiras_filter(request):
    operador = operator.or_ if request.GET.get("operador", "and") == "or" else operator.and_
    filtros = filtros_compostos(request.GET, operador)
    return feira_get(Feira.objects.filter(filtros))


def filtros_compostos(filtros, operador):
    q_list = [Q((CAMPOS_BUSCA[filtro] + "__contains", valor))
              for filtro, valor in filtros.iteritems() if filtro in CAMPOS_BUSCA]
    try:
        return reduce(operador, q_list)
    except TypeError:
        raise DadosInvalidos(
            u"Parâmetros de busca incorretos ou não definidos. "
            u"Campos disponiveis para busca: " + ", ".join([c for c in CAMPOS_BUSCA])
        )


def adicionar_feira(request):
    post_body = feira_nova_valida(request)
    return Feira.objects.create(**post_body)


def feira_nova_valida(request):
    post_body = json.loads(request.body)
    return validar_campo_relacionado(
        validar_campo_relacionado(
            validar_id(
                validar_campos_obrigatorios(post_body)
            ), "distrito", Distrito
        ), "subprefeitura", Subprefeitura
    )


def validar_campos_obrigatorios(post_body):
    post_body, erros = campos_obrigatorios_preenchidos(post_body, CAMPOS_OBRIGATORIOS)
    if not post_body:
        raise DadosInvalidos(
            u"Os seguintes campos obrigatórios não foram preenchidos: {}".format(", ".join(erros))
        )
    return post_body


def campos_obrigatorios_preenchidos(post_body, campos_obrigatorios):
    erros = []
    result = post_body
    for campo in campos_obrigatorios:
        if not post_body.get(campo):
            erros.append(campo)
            result = False
    return result, erros


def validar_id(post_body):
    if not post_body.get("id"):
        return post_body

    try:
        Feira.objects.get(id=int(post_body.get("id")))
    except Feira.DoesNotExist:
        return post_body

    raise DadosInvalidos(u"O id informado já existe no cadastro de feiras")


def feira_put_id(request, id):
    return feira_patch_id(request, id)


def feira_patch_id(request, id):
    feira_obj = Feira.objects.get(id=id)
    alteracoes = alteracoes_validas(json.loads(request.body), id)
    return feira_patch(request, feira_obj, alteracoes)


def feira_patch(request, feira_obj, alteracoes):
    for campo, valor in alteracoes.iteritems():
        if campo not in CAMPOS_OBRIGATORIOS or valor is not None:
            setattr(feira_obj, campo, valor)
    feira_obj.save()
    return feira_get_id(None, feira_obj.id)


def alteracoes_validas(alteracoes, id):
    return validar_campo_relacionado(
        validar_campo_relacionado(
            alteracoes_id_valido(
                alteracoes, id
            ), "distrito", Distrito
        ), "subprefeitura", Subprefeitura
    )


def alteracoes_id_valido(alteracoes, id):
    novo_id = alteracoes.get("id")
    if novo_id and (int(novo_id) != int(id)):
        raise DadosInvalidos(u"Campo id não pode ser alterado: {} => {}".format(id, novo_id))
    return alteracoes


def validar_campo_relacionado(campos, campo, model_class):
    campo_nome = campo + "_nome"
    codigo = campos.get(campo + "_id")
    if not codigo:
        return campos

    if not campos.get(campo_nome):
        validar_codigo_relacionado(campo, model_class, codigo)
        return campos

    try:
        model_class.objects.get_or_create(codigo=codigo, nome=campos.get(campo_nome))
    except IntegrityError:
        raise DadosInvalidos(u"Já existe {} código {} com nome diferente do informado".format(campo, codigo))

    del(campos[campo_nome])
    return campos


def validar_codigo_relacionado(campo, model_class, codigo):
    try:
        model_class.objects.get(codigo=codigo)
    except model_class.DoesNotExist:
        raise DadosInvalidos(u"O código informado para {} não existe".format(campo))


def feira_get_id(request, id):
    return feira_get(Feira.objects.get(id=id))


def feira_get(objeto_ou_lista):
    t = type(objeto_ou_lista)
    lista = objeto_ou_lista if t == list or t == QuerySet else [objeto_ou_lista]
    return JsonResponse(serializar_feiras(lista))


def feira_delete_id(request, id):
    feira_obj = Feira.objects.get(id=id)
    feira_obj.delete()
    return status_response(200, u"Feira {} removida com sucesso".format(id))


def serializar_feiras(feiras_list):
    return {
        "count": len(feiras_list),
        "results": [feira_to_dict(feira_obj) for feira_obj in feiras_list],
    }


def feira_to_dict(feira_obj):
    return dict(
        {k: v for k, v in feira_obj.__dict__.iteritems() if not k.startswith("_")},
        **{
            "subprefeitura_nome": feira_obj.subprefeitura.nome,
            "distrito_nome": feira_obj.distrito.nome,
        }
    )


def validar_metodo(metodo, permitidos):
    if metodo not in permitidos:
        raise MetodoNaoPermitido(u"O método {} não é permitido para este recurso".format(metodo))


def metodo_nao_permitido(erro):
    return status_response(405, unicode(erro))


def status_response(status, message):
    return JsonResponse({
        "status": status,
        "message": message,
    }, status=status)


metodos = {
    "GET": feira_get_id,
    "DELETE": feira_delete_id,
    "PUT": feira_put_id,
    "PATCH": feira_patch_id,
}
