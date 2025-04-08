from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm

from .models import Conta, Transacao, Categoria
from .forms import ContaForm, TransacaoForm, CategoriaForm


def home(request):
    if request.user.is_authenticated:
        contas = Conta.objects.filter(usuario=request.user)
        conta = None
        for conta in contas:
            # Calcular receitas e despesas para cada conta
            receitas = Transacao.objects.filter(conta=conta, categoria__tipo='REC').aggregate(Sum('valor'))['valor__sum'] or 0
            despesas = Transacao.objects.filter(conta=conta, categoria__tipo='DSP').aggregate(Sum('valor'))['valor__sum'] or 0
            conta.saldo = receitas - despesas  # Saldo da conta

        # Obter saldo global atual
        saldo_atual = 0
        for conta in contas:
            for transacao in Transacao.objects.filter(conta=conta):
                if transacao.tipo == 'REC':
                    saldo_atual += transacao.valor
                else:
                    saldo_atual -= transacao.valor

        """
        saldo_atual = sum([
            transacao.valor if transacao.tipo == 'REC' else - transacao.valor            
            for conta in contas
            for transacao in Transacao.objects.filter(conta=conta)
        ])
        """
        
        receitas_mes = 0
        despesas_mes = 0
        for conta in contas:
            receitas_mes += Transacao.objects.filter(conta=conta, categoria__tipo='REC').aggregate(Sum('valor'))['valor__sum'] or 0

            despesas_mes += Transacao.objects.filter(conta=conta, categoria__tipo='DSP').aggregate(Sum('valor'))['valor__sum'] or 0


        transacoes = Transacao.objects.filter(conta__usuario=request.user)
        print(transacoes)

        
        
        if request.method == 'POST' and 'excluir_transacao_id' in request.POST:
            transacao_id = request.POST.get('excluir_transacao_id')
            transacao = get_object_or_404(Transacao, id=transacao_id, conta__usuario=request.user)
            transacao.delete()

        return render(request, 'controle/home.html', {
            'saldo_atual': saldo_atual,
            'contas': contas,
            'receitas_mes': receitas_mes,
            'despesas_mes': despesas_mes,
            'transacoes': transacoes,
        })
    return redirect('login')


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'controle/cadastrar_usuario.html', {'form': form})


def cadastrar_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            return redirect('home')
    else:
        form = ContaForm()
    return render(request, 'controle/cadastrar_conta.html', {'form': form})


def registrar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST, user=request.user)  # Passa o usuário para o formulário
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.save()  # Salva a transação sem associá-la a uma conta ainda
            return redirect('home')
    else:
        form = TransacaoForm(user=request.user)  # Passa o usuário para o formulário
    return render(request, 'controle/registrar_transacao.html', {'form': form})

def excluir_transacao(request, transacao_id):
    if request.user.is_authenticated:
        try:
            # Obtém a transação pelo ID
            transacao = get_object_or_404(Transacao, pk=transacao_id,  conta__usuario=request.user)
            
            # Verifica se a transação pertence a uma conta do usuário autenticado
            if transacao.conta.usuario != request.user:
                return redirect('home')  # Redireciona se o usuário não for o dono
            
            transacao.delete()  # Exclui a transação
            return redirect('home')  # Redireciona para a página inicial após a exclusão
        except Exception as e:
            print(f'Erro ao tentar excluir a transação: {e}')
            return redirect('home')  # Ou outra ação desejada
    return redirect('cadastrar_usuario')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a página de cadastro após o logout

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()
    return render(request, 'controle/login.html', {'form': form})

def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # Salva a nova categoria
            return redirect('home')  # Redireciona para a página inicial
    else:
        form = CategoriaForm()  # Cria uma instância vazia do formulário
    return render(request, 'controle/cadastrar_categoria.html', {'form': form})