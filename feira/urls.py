from django.conf.urls import url
from .views import feiras, feira


urlpatterns = [
    url(r"^v1.0/feiras/$", feiras, name="api-feiras-list"),
    url(r"^v1.0/feiras/(?P<id>\d+)/$", feira, name="api-feiras-list"),
]