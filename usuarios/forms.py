from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserChangeForm(UserChangeForm):
    class Meta(type(UserChangeForm)):
        model = CustomUser
        cleaned_data = ['nome', 'username', 'escola', 'turma', 'cargo', 'password']  # You can specify the fields you want to include/exclude here
        fields = ('nome', 'username', 'escola', 'turma', 'cargo', 'password')
        labels = {
            'password': 'Senha'  # Define o rótulo do campo de senha como "Senha"
        }
        
class CustomUserCadastroForm(UserCreationForm):
    class Meta(type(UserCreationForm)):
        model = CustomUser
        cleaned_data = ['nome', 'username', 'escola', 'turma', 'cargo', 'password']  # You can specify the fields you want to include/exclude here
        fields = ('nome', 'username', 'escola', 'turma', 'cargo', 'password')
        labels = {
            'password': 'Senha'  # Define o rótulo do campo de senha como "Senha"
        }
        widgets = {
            'password': forms.PasswordInput(),  # Para mascarar a entrada da senha no HTML
        }

class CustomLoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput())