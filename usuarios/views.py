from django.http import HttpResponse
import imaplib
from rolepermissions.decorators import has_permission_decorator
from .forms import CustomUserChangeForm, CustomUserCadastroForm
from .models import CustomUser
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404, render, redirect #redireciona para uma página -> espera url
from django.contrib.auth import authenticate, login 
from django.contrib import auth, messages
from .admin import CustomUserAdmin
from django.urls import reverse # passar o nome da url e ele faz a transformação para o caminho
from .serializers import CustomUserSerializer
from rest_framework.response import Response
from django.contrib import messages
from django.views import View
from .models import CustomUser

# Create your views here.
def home(request):
    users = CustomUser.objects.all()
    return render(request, 'home.html', {'users': users})

# CADASTRAR  (CREATE) ALUNO, TESTADO OK
@has_permission_decorator('cadastrar_aluno')
def cadastrar_aluno(request):
    if request.method == 'GET':
        alunos = CustomUser.objects.filter(cargo='A') # select * from CustomUser where cargo = 'A'
        return render(request, 'cadastrar_aluno.html', {'alunos': alunos})
    if request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        password = request.POST.get('password')
        escola = request.POST.get('escola')
        turma = request.POST.get('turma')
        
        user = CustomUser.objects.filter(username=username)
        
        if user.exists():
                #messages.error(request, "Este CPF, do aluno, já é registrado.")
            return HttpResponse("CPF já registrado.")
            
        user = CustomUser.objects.create(nome=nome, username=username, password=password, cargo='A', escola=escola, turma=turma)
        # TODO: confirmar o redirecionar com uma mensagem
        
        return HttpResponse("Cadastro realizado com sucesso!")

@has_permission_decorator('cadastrar_gestor')
def cadastrar_gestor(request):
    if request.method == 'GET':
        gestor = CustomUser.objects.filter(cargo='G')
        return render(request, 'cadastrar_gestor.html', {'gestor': gestor})
    if request.method == 'POST':
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

# TESTADO OK
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            #return redirect(reverse('home'))
            return render(request, 'login.html')
    elif request.method == 'POST':
        login = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=login, password=password)

        if not user:
            #TODO: redirecionar com msg de erro
            return HttpResponse("CPF ou senha inválido.")

        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Login realizado com sucesso!')
        return redirect(reverse('home'))

def logout(request):
    request.session.flush()
    return redirect(reverse('login'))

# LER (READ)
# LISTAR ALUNOS, 
@has_permission_decorator('cadastrar_aluno')
def listar_alunos(request):
    aluno = CustomUser.objects.filter(cargo='A')
    return render(request, 'listar_alunos.html', {'aluno': aluno})

# LISTAR GESTORES, 
@has_permission_decorator('cadastrar_aluno')
def listar_gestores(request):
    gestor = CustomUser.objects.filter(cargo='G')
    return render(request, 'listar_gestores.html', {'gestor': gestor})


# EDITAR (UPDATE)
@has_permission_decorator('cadastrar_aluno')
def editar_aluno(request, username):
    aluno = get_object_or_404(CustomUser, username=username)
    if request.method == 'GET':
        form = CustomUserChangeForm(instance=aluno)
        return render(request, '(?).html', {'form': form, 'aluno': aluno})
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST or None, instance=aluno)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Aluno atualizado com sucesso!')
            return redirect(reverse('cadastrar_aluno'))
        else:
            return render(request, '(?).html', {'form': form, 'aluno': aluno})

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
    if request.method == 'POST':
        aluno.delete()
        messages.add_message(request, messages.SUCCESS, 'Aluno excluído com sucesso!')
    return redirect(reverse('cadastrar_aluno'))