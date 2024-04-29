from rolepermissions.roles import AbstractUserRole

#as permissões de available_permissions são as permissões que o usuário terá e devem ser criadas como def nas views

class Gestor(AbstractUserRole):
    available_permissions = {
        'cadastrar_aluno': True,
        'cadastrar_gestor': True,
        'login': True,
        #'alterar_dados_alunos': True,
        #'cadastrar_turma': True,
        #'deletar_turma': True,
        #'atualizar_turma': True,
        #'ler_turma': True,
        #'atualizar_escola': True,
        #'ler_escola': True,
    }
    
class Aluno(AbstractUserRole):
    available_permissions = {
        'login': True,
        #'alterar_dados_alunos': True,
        #'ler_aluno': True,
    }