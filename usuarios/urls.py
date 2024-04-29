from django.urls import path 
from usuarios import views

urlpatterns = [
    path('cadastrar_aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('cadastrar_gestor/', views.cadastrar_gestor, name='cadastrar_gestor'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name="logout"),
    path('editar_aluno/<str:cpf>/', views.editar_aluno, name='editar_aluno'),
    path('incluir_aluno/', views.incluir_aluno, name='incluir_aluno'),
    path('excluir_aluno/<str:cpf>/', views.excluir_aluno, name='excluir_aluno')

]