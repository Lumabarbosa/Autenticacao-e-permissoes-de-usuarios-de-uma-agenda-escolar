from django.urls import path 
from usuarios import views
from django.views.generic import View
from .models import CustomUser
from .views import SignUpView
from django.views.generic.base import TemplateView

urlpatterns = [
    path("signup/", SignUpView, name="signup"),
    path('home/', views.home, name='home'),
    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('cadastrar_gestor/', views.cadastrar_gestor, name='cadastrar_gestor'),
    path('logout/', views.logout, name='logout'),
    path('editar_aluno/<str:username>/', views.editar_aluno, name='editar_aluno'),
    path('incluir_aluno/', views.incluir_aluno, name='incluir_aluno'),
    path('excluir_aluno/<str:username>/', views.excluir_aluno, name='excluir_aluno'),
]