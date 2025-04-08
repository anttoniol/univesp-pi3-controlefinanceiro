from django.urls import path
from .views import home, cadastrar_usuario, cadastrar_conta, registrar_transacao, logout_view, cadastrar_categoria, login_usuario

urlpatterns = [
    path('', home, name='home'),
    path('cadastrar_usuario/', cadastrar_usuario, name='cadastrar_usuario'),
    path('cadastrar_conta/', cadastrar_conta, name='cadastrar_conta'),
    path('registrar_transacao/', registrar_transacao, name='registrar_transacao'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_usuario, name='login'),
    path('cadastrar_categoria/', cadastrar_categoria, name='cadastrar_categoria'),
]

