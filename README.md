# AgendaSeducFinal
Back-end Autenticação e permissões de usuários

Este projeto foi feito com:

https://www.python.org/

https://www.djangoproject.com/

https://www.django-rest-framework.org/


Como rodar o projeto?

Clone esse repositório.
Crie um virtualenv com Python 3.
python -m venv venv
Ative o virtualenv.
.venv/bin/activate 
Instale as dependências.
requirements.txt
Rode as migrações.
python manage.py makemigrations
python manage.py migrate

pip install virtualenv # Windows
virtualenv nome_do_ambiente # Windows
nome_do_ambiente\Scripts\activate # Windows
python -m venv .venv # Linux
source .venv/bin/activate  # Linux

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser (já foi criado), as credenciais estão em um arquvo txt na pasta do projeto.


Links de consulta

https://www.youtube.com/watch?v=EoJd5EIXtKU&list=PL3gEA6Xsr_enXqFtBYxenjSqURqmNzRPN&index=2

https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

