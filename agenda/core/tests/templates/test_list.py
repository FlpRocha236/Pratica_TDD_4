from django.contrib.auth import get_user_model ### AJUSTE 1: Importar get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

User = get_user_model()

class List_Contact_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@fatec.sp.gov.br', 
            password='fatec'
        )
        
        self.login_url = reverse('login')
        self.list_url = reverse('listar') 
        
        self.agenda = Agenda.objects.create(
            nome_completo='Felipe Teste 1',
            telefone='19999991111',
            email='felipe1.teste@fatec.sp.gov.br',
            observacao='teste'
        )
        self.agenda2 = Agenda.objects.create(
            nome_completo='Felipe Teste 2',
            telefone='19999992222',
            email='felipe2.teste@fatec.sp.gov.br',
            observacao='teste 2'
        )
        
    def test_Not_Logged_List_Template(self):
        response = self.client.get(self.list_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'{self.login_url}?next={self.list_url}')
    
    def test_Logged_List_Template(self):
        self.client.login(username='admin', password='fatec')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'listar.html')

    def test_list_contacts(self):
        self.client.login(username='admin', password='fatec')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'listar.html')
        
      
        self.assertContains(response, 'Felipe Teste 1')
        self.assertContains(response, 'Felipe Teste 2')
        self.assertContains(response, '19999991111')
        self.assertContains(response, '19999992222')
        self.assertContains(response, 'felipe1.teste@fatec.sp.gov.br')
        self.assertContains(response, 'felipe2.teste@fatec.sp.gov.br')

    def test_list_contacts_empty(self):
        self.client.login(username='admin', password='fatec')
        Agenda.objects.all().delete()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'listar.html')
        self.assertContains(response, 'Nenhum contato encontrado.')
      
        self.assertNotContains(response, 'Felipe Teste 1')
        self.assertNotContains(response, 'Felipe Teste 2')
        self.assertNotContains(response, '19999991111')
        self.assertNotContains(response, '19999992222')