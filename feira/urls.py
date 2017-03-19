from django.conf.urls import url
from .views import feiras, feira, feiras_busca


urlpatterns = [
    url(r"^v1.0/feiras/$", feiras, name="api-feiras"),
    url(r"^v1.0/feiras/busca/$", feiras_busca, name="api-feiras-search"),
    url(r"^v1.0/feiras/(?P<id>\d+)/$", feira, name="api-feira-id"),
]
