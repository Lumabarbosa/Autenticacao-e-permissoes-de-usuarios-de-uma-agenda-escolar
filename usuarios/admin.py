from multiprocessing import process
from django.contrib import admin, messages
from .models import CustomUser
from django.contrib.auth import admin as auth_admin_django
from .forms import CustomUserChangeForm, CustomUserCadastroForm
import importlib.util
import sys
import csv
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.forms import forms
from django.http import HttpResponseRedirect, HttpResponse

class CsvUserForm(forms.Form):
    csv_upload = forms.FileField()

@admin.register(CustomUser)
class CustomUserAdmin(auth_admin_django.UserAdmin):
    form = CustomUserChangeForm
    add_form =  CustomUserCadastroForm
    model = CustomUser
    fieldsets = auth_admin_django.UserAdmin.fieldsets + (
        ('Custom Fields', {
            "fields": (
                "nome",
                "cargo",
                "escola",
                "turma",
            ),
        }),
    )
    list_display = ["nome", "username", "escola", "turma", "cargo", "password"]
    

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    
    print('passei1')
    def upload_csv(self, request):
        form = CsvUserForm(request.POST, request.FILES)
        print("passo 2")
           
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Error, CSV File required.')
                return HttpResponseRedirect(request)
               
            df = pd.read_csv(csv_file)
            print('Passei 3: df')
            print(df)
            
            for _, row in df.iterrows():
                # Itera sobre as linhas do DataFrame lido do arquivo Excel
                # Use get_or_create para evitar a necessidade de verificar a existência antes de criar
                user, created = CustomUser.objects.get_or_create(
                    username=row['username'],
                    password=row['password'],
                    defaults={
                        'nome': row['nome'],
                        'escola': row['escola'],
                        'turma': row['turma'],
                        'cargo': row['cargo'],
                    }
                )
            print("passei 7")
            messages.success(request, 'CSV File imported successfully')
        return render(request, "admin\csv_upload.html", {"form": form})
    
