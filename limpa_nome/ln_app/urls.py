from django.urls import path
from . import views

urlpatterns = [
    path("acordo_efetivado/", views.hook_acordo_efetivado, name="acordo_efetivado"),
    path("acordo_quebrado/", views.hook_acordo_quebrado, name="acordo_quebrado"),
    path("acordo_quitado/", views.hook_acordo_quitado, name="acordo_quitado"),
    path("pagamento_parcela/", views.hook_pagamento_parcela, name="pagamento_parcela"),
    path("inclusao_divida/", views.hook_inclusao_divida, name="inclusao_divida"),
    path("remocao_divida/", views.hook_remocao_divida, name="remocao_divida"),
    path("obter_boleto/", views.obter_boleto, name="obter_boleto"),
]