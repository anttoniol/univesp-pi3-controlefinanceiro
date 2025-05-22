from django.db import models
from django.contrib.auth.models import User

class Conta(models.Model):
    TIPO_CONTA = [
        ('CC', 'Conta Corrente'),
        ('CP', 'Conta Poupança'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, choices=TIPO_CONTA)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Categoria(models.Model):
    TIPOS = [
        ('REC', 'Receita'),
        ('DSP', 'Despesa'),
    ]
    tipo = models.CharField(max_length=3, choices=TIPOS)  # Tipo da categoria, 'RECEITA' ou 'DESPESA'
    nome = models.CharField(max_length=50)  # Nome da categoria, ex: 'Alimentação'

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Transacao(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  # Relacionamento com Categoria
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.categoria.tipo}: {self.valor} em {self.data} ({self.categoria.nome})"
    @property
    def tipo(self):
        return self.categoria.tipo if self.categoria else None

