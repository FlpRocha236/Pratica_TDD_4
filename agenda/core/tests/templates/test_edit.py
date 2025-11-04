from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

User = get_user_model()

class Atualizar_Contact_OK_Test(TestCase):
    def setUp(self):
        self.client = Client() 
        
        self.user = User.objects.create_user(
            username='admin',
            email='admin@fatec.sp.gov.br', 
            password='fatec'
        )
        
        self.login_url = reverse('login')
        
        self.agenda = Agenda.objects.create(
            nome_completo='felipe test',
            telefone='19999768070',
            email='felipe.teste@fatec.sp.gov.br',
            observacao=''
        )
        
        self.atualizar_url = reverse('atualizar_contato', kwargs={'id': self.agenda.pk})
        
    def test_Not_Logged_Edit_Template(self):
        response = self.client.get(self.atualizar_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'{self.login_url}?next={self.atualizar_url}')

    def test_Logged_Edit_Template(self):
        self.client.login(username='admin', password='fatec')
        response = self.client.get(self.atualizar_url) 
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'atualizar.html')
    
    def test_edit_post_data(self):
        self.client.login(username='admin', password='fatec')
        data= {
            'nome_completo' : 'felipe test atualizar',
            'telefone' : '19999768070',
            'email' : 'felipe.atualizar@fatec.sp.gov.br',
            'observacao' : 'teste atualizar'
        }

        response = self.client.post(self.atualizar_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND) 
        self.assertRedirects(response, reverse('home')) 
        self.agenda.refresh_from_db()
        
        # ### AJUSTE AQUI ###
        # O nome procurado deve ser o mesmo que você enviou no 'data'
        self.assertTrue(Agenda.objects.filter(nome_completo='felipe test atualizar').exists())

    def test_edit_post_invalid_data(self):
        self.client.login(username='admin', password='fatec')
        data= {
            'nome_completo' : '',
            'telefone' : 'error',
            'email' : '',
            'observacao' : 'teste'
        }
        response = self.client.post(self.atualizar_url, data) 
        self.assertEqual(response.status_code, HTTPStatus.OK) 
        self.assertTemplateUsed(response, 'atualizar.html') 
        
        self.assertContains(response, 'Nome completo: Este campo é obrigatório.')
        self.assertContains(response, 'O telefone deve conter apenas')
        self.assertContains(response, 'Email: Este campo é obrigatório.')
        
        self.assertFalse(Agenda.objects.filter(telefone='error').exists())
        self.assertTrue(Agenda.objects.filter(nome_completo='felipe test').exists())

    def test_edit_post_no_data(self):
        self.client.login(username='admin', password='fatec')
        response = self.client.post(self.atualizar_url, {}) 
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'atualizar.html') 
        self.assertTrue(Agenda.objects.filter(nome_completo='felipe test').exists())

    def test_edit_post_invalid_id(self):
        self.client.login(username='admin', password='fatec')
        
        invalid_url = reverse('atualizar_contato', kwargs={'id': 99999})
        
        # ### AJUSTE AQUI ###
        # Os dados devem ser válidos para que o teste foque apenas no ID inválido
        data= {
            'nome_completo' : 'felipe test 999',
            'telefone' : '19999768070',
            'email' : 'felipe.rocha29@fatec.sp.gov.br',
            'observacao' : 'teste atualizar'
        }
 
        response = self.client.post(invalid_url, data)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Agenda.objects.filter(nome_completo='felipe test').exists())