# Back-end da Autenticação e permissões de usuários da Agenda Escolar para Seduc-PE

## Descrição 

Este projeto é uma agenda escolar elaborada com o intuito de realizar a autenticação do usuário no banco de dados a partir do cpf do aluno digitado pelo próprio aluno ou responsável no login, ou através da importação de um arquivo csv através de usuário 'gestor'.

## Instalação

- Python 3.12.
- Django.
- Crie um amviente virtual.
- Bibliotecas Python: django, rest-framework, role-permissions, openpyxl, sqlparse.

### Como rodar o projeto?

- Clone esse repositório.

- Crie um virtualenv com Python 3.
    - pip install virtualenv # Windows
    - python -m venv .venv # Linux

- Ative o virtualenv.
    - nome_do_ambiente\Scripts\activate # Windows
    - source .venv/bin/activate  # Linux

- Instale as dependências.
    - pip install -r requirements.txt

- Rode as migrações.
    - python manage.py makemigrations
    - python manage.py migrate

- python manage.py createsuperuser (já foi criado), as credenciais estão em um arquvo txt na pasta do projeto.

### Links de consulta

https://www.youtube.com/watch?v=EoJd5EIXtKU&list=PL3gEA6Xsr_enXqFtBYxenjSqURqmNzRPN&index=2

https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

