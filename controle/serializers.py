from django.contrib.auth.models import Group, User
from .models import Conta, Categoria, Transacao
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ContaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conta
        fields = ['usuario', 'nome', 'tipo']


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categoria
        fields = ['tipo', 'nome']


class TransacaoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transacao
        fields = ['conta', 'categoria', 'data', 'valor']