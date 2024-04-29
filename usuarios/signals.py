from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser
from rolepermissions.roles import assign_role

#IMPORTAR NO APP
@receiver(post_save, sender=CustomUser)
def define_permissoes(sender, instance, created, **kwargs):
    if created:
        if instance.cargo == 'G':
            assign_role(instance, 'gestor')
        elif instance.cargo == 'A':
            assign_role(instance, 'aluno')