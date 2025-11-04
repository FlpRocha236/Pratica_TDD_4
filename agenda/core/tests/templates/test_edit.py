from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

class Edit_Contact_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()  # Cria um cliente de teste que simula requisições HTTP
        
        # Cria um usuário de teste (admin)
        new_user = User.objects.create(email='admin@fatec.sp.gov.br', username='admin')
        new_user.set_password('fatec')  # Define a senha do usuário
        new_user.save()  # Salva o usuário no banco de dados de teste
        
        # URLs usadas nos testes
        self.login_url = reverse('login')          # URL da página de login
        self.edit_url = reverse('edit_contact')    # URL da view de edição de contato
        
        # Cria um contato de teste na tabela Agenda
        self.agenda = Agenda.objects.create(
            nome_completo='jamila test',
            telefone='19991555845',
            email='jamila.teste@fatec.sp.gov.br',
            observacao=''
        )
        
    def test_Not_Logged_Edit_Template(self):
        # Testa acesso sem login: deve redirecionar para a página de login
        response = self.client.get(self.edit_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)  # Usuário não deve ter acesso
        self.assertRedirects(response, f'{self.login_url}?next={self.edit_url}')  # Redireciona para login com parâmetro "next"

    def test_Logged_Edit_Template(self):
        # Testa acesso com login
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Deve carregar normalmente
        self.assertTemplateUsed(response, 'edit_contact.html')  # Usa o template correto
    
    def test_edit_post_data(self):
        # Testa envio de dados válidos para editar um contato existente
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        data= {
            'id': self.agenda.pk,
            'nome_completo' : 'jamila test edit',
            'telefone' : '19991555845',
            'email' : 'jamila.edit@fatec.sp.gov.br',
            'observacao' : 'teste edit'
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # Espera redirecionamento (status 302)
        self.assertRedirects(response, reverse('home'))  # Após editar, deve ir para a página inicial
        self.agenda.refresh_from_db()  # Atualiza o objeto com os dados mais recentes do banco
        self.assertTrue(Agenda.objects.filter(nome_completo='jamila test edit').exists())  # Confirma que o nome foi alterado

    def test_edit_post_invalid_data(self):
        # Testa envio de dados inválidos (faltando campos obrigatórios ou com formato incorreto)
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        data= {
            'id': self.agenda.pk,
            'nome_completo' : '',        # Nome vazio
            'telefone' : 'error',        # Telefone inválido
            'email' : '',                # Email vazio
            'observacao' : 'teste'
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Não redireciona — permanece na página
        self.assertTemplateUsed(response, 'edit_contact.html')  # Renderiza o mesmo template
        # Verifica se as mensagens de erro esperadas aparecem no HTML
        self.assertContains(response, 'Nome Completo: Informe o nome completo')
        self.assertContains(response, 'O telefone deve conter apenas')
        self.assertContains(response, 'E-Mail: Informe o e-mail')
        # Garante que os dados inválidos NÃO foram salvos no banco
        self.assertFalse(Agenda.objects.filter(telefone='error').exists())
        # E o registro original continua existindo
        self.assertTrue(Agenda.objects.filter(nome_completo='jamila test').exists())

    def test_edit_post_no_data(self):
        # Testa envio de formulário vazio
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        response = self.client.post(self.edit_url, {})
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Continua na mesma página
        self.assertTemplateUsed(response, 'edit_contact.html')  # Mesmo template
        # Confirma que o registro original não foi alterado
        self.assertTrue(Agenda.objects.filter(nome_completo='jamila test').exists())

    def test_edit_post_invalid_id(self):
        # Testa envio de um ID que não existe na base de dados
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        data= {
            'id': 99999,  # ID inexistente
            'nome_completo' : 'jamila test edit',
            'telefone' : '19991555845',
            'email' : 'jamila.moraes@fatec.sp.gov.br',
            'observacao' : 'teste edit'
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)  # Não redireciona (view deve tratar o erro)
        self.assertTemplateUsed(response, 'edit_contact.html')  # Renderiza o mesmo template
        # Confirma que o contato original ainda existe e não foi alterado
        self.assertTrue(Agenda.objects.filter(nome_completo='jamila test').exists())
