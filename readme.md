# Instruções

1. Criar ambente virtual: `python -m venv nome-ambiente-virtual`
2. Ativar ambiente virtual: 
	1. Linux: `source nome-ambiente-virtual/bin/activate`
	2. Windows: `nome-ambiente-virtual/Scripts/Activate`
3. Instalar Django no ambiente virtual: `pip install django`
4. Executar os comandos:
	1. `python manage.py makemigrations`
	2. `python manage.py migrate`
5. (Opcional) Criar superusuário: `python manage.py createsuperuser`
6. Subir a aplicação: `python manage.py runserver`
7. (Opcional) Para acessar a API para obtenção de dados, acessar http://127.0.0.1:8000/stats/ , usando os dados de superusuário criado no passo 5.

