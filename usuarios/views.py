from django.http import HttpResponse
import imaplib
from rolepermissions.decorators import has_permission_decorator, has_role_decorator
from .forms import CustomUserChangeForm, CustomUserCadastroForm
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, render, redirect #redireciona para uma página -> espera url
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from .admin import CustomUserAdmin
from django.urls import reverse # passar o nome da url e ele faz a transformação para o caminho
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from django.contrib import messages
from django.views import View
from .models import CustomUser
from django.urls import reverse_lazy

from usuarios.signals import define_permissoes
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.permissions import grant_permission
from django.contrib.auth import get_user_model
from django.views import generic

def get_queryset(self):
    return super(CustomUserAdmin).get_queryset()


def home(request):
    #grant_permission(request.user, 'login')
    print(get_user_roles(request.user))
    return render(request, "home.html")

# CADASTRAR  (CREATE) ALUNO,  c/ permissões, TESTADO OK
@has_permission_decorator('cadastrar_aluno')
def cadastrar_aluno(request):
    if request.method == 'GET':
            alunos = CustomUser.objects.filter(cargo='A')
            return render(request, 'cadastrar_aluno.html', {'alunos': alunos})
    if request.method == 'POST' or request.method == 'FILES':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        password = request.POST.get('password')
        escola = request.POST.get('escola')
        
        user = CustomUser.objects.filter(username=username)
        
        if user.exists():
                #messages.error(request, "Este CPF, do aluno, já é registrado.")
            return HttpResponse("CPF já registrado.")
            
        user = CustomUser.objects.create(nome=nome, username=username, password=password, cargo='A', escola=escola) 
        user.save()
        #messages.success(request, "Cadastro realizado com sucesso!")
        return HttpResponse("Cadastro de aluno realizado com sucesso!")

# CADASTRAR  (CREATE) Gestor c/ permissões, TESTADO OK
@has_permission_decorator('cadastrar_gestor')
def cadastrar_gestor(request):
    if request.method == 'GET':
        gestores = CustomUser.objects.filter(cargo='G')
        return render(request, 'cadastrar_gestor.html', {'gestores': gestores})
    if request.method == 'POST' or request.method == 'FILES':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        password = request.POST.get('password')
        escola = request.POST.get('escola')
        
        user = CustomUser.objects.filter(username=username)
        
        if user.exists():
                #messages.error(request, "Este CPF, do aluno, já é registrado.")
            return HttpResponse("CPF já registrado.")
            
        user = CustomUser.objects.create(nome=nome, username=username, password=password, cargo='G', escola=escola) 
        # TODO: confirmar o redirecionar com uma mensagem
        #messages.success(request, "Cadastro realizado com sucesso!")
        return HttpResponse("Cadastro de gestor realizado com sucesso!")

@has_role_decorator('aluno', 'gestor')
class SignUpView(generic.CreateView):
    form_class = CustomUserCadastroForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def logout(request):
    request.session.flush()
    return redirect(reverse('login'))


# LER (READ)
# LISTAR ALUNOS, 
@has_permission_decorator('cadastrar_aluno')
def listar_alunos(request):
    alunos = CustomUser.objects.filter(cargo='A')
    return render(request, 'listar_alunos.html', {'alunos': alunos})

# LISTAR GESTORES, 
@has_permission_decorator('cadastrar_aluno')
def listar_gestores(request):
    gestores = CustomUser.objects.filter(cargo='G')
    return render(request, 'listar_gestores.html', {'gestores': gestores})


# EDITAR (UPDATE)
@has_permission_decorator('cadastrar_aluno')
def editar_aluno(request, username):
    aluno = get_object_or_404(CustomUser, username=username)
    if request.method == 'GET':
        form = CustomUserChangeForm(instance=aluno)
        return render(request, 'cadastrar_aluno.html', {'form': form, 'aluno': aluno})
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST or None, instance=aluno)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Aluno atualizado com sucesso!')
            return redirect(reverse('cadastrar_aluno'))
        else:
            return render(request, 'cadastrar_aluno.html', {'form': form, 'aluno': aluno})

#Dúvida: Em "return render(request, '(?).html', {'form': form, 'aluno': aluno})" direciona para "cadastrar_aluno.html"?
#Em else: " return render(request, '(?).html', {'form': form, 'aluno': aluno})"direciona para "cadastrar_aluno.html"?

@has_permission_decorator('cadastrar_aluno')
def incluir_aluno(request):
    if request.method == 'GET':
        form = CustomUserCadastroForm()
        return render(request, 'incluir_aluno.html', {'form': form})
    elif request.method == 'POST':
        form = CustomUserCadastroForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Aluno incluído com sucesso!')
            return redirect(reverse('cadastrar_aluno'))
        else:
            return render(request, 'incluir_aluno.html', {'form': form})


#Dúvida: Em "return render(request, '(?)_aluno.html', {'form': form})" direciona para "cadastrar_aluno.html"?
         #Em else: " return render(request, '(?)_aluno.html', {'form': form})" direciona para "cadastrar_aluno.html"?


#Em "incluir_aluno",a função não recebe um CPF porque está criando um novo aluno, e o CPF será fornecido pelo usuário através do formulário de inclusão de aluno.
#Em "excluir_aluno" e "editar_aluno", as funções precisam de um CPF porque estão operando com um aluno existente,o CPF é usado para identificar qual aluno deve ser editado ou excluído.

# EXCLUIR (DELETE)
# TESTADO OK
@has_permission_decorator('cadastrar_aluno')
def excluir_aluno(request, username):
    aluno = get_object_or_404(CustomUser, username=username)
    print("passei exc 1")
    if request.method == 'POST':
        print("passei exc 2")
        aluno.delete()
        print("passei exc 3")
        messages.add_message(request, messages.SUCCESS, 'Aluno excluído com sucesso!')
    return redirect(reverse('cadastrar_aluno'))