from django.urls import include, path
from rest_framework import routers

from .views_stats import *

router = routers.DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'grupos', GroupViewSet)
router.register(r'contas', ContaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'transacoes', TransacaoViewSet)


urlpatterns = [
    path('stats/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]