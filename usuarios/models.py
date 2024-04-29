from django.db import models
from cpf_field.models import CPFField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework import status
choices_cargo = (('G', 'Gestor'),
                    ('A', 'Aluno'))


class CustomUser(AbstractUser):
    
    nome = models.CharField(max_length=150, null=True, blank=False, default='')
    username = CPFField(primary_key=True, null=False, blank=False, help_text='Informe o CPF sem pontos ou traços', default='00000000000')
    escola = models.CharField(max_length=100, null=True, blank=True)
    turma = models.CharField(max_length=10)
    cargo = models.CharField(max_length=1, choices=choices_cargo, default='')
    password = models.CharField(max_length=150, null=False, blank=False, default='')
    
    REQUIRED_FIELDS = ['nome', 'escola', 'turma', 'cargo', 'password']
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'
    
    def __str__(self):
        return self.username
    