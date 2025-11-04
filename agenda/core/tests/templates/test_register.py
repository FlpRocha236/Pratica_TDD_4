from django.contrib.auth import get_user_model ### AJUSTE 1: Importar get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

User = get_user_model() 

class Register_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@fatec.sp.gov.br', 
            password='fatec'
        )
        
        self.login_url = reverse('login')
        self.register_url = reverse('cadastrar')

    def test_Not_Logged_Register_Template(self):
        response = self.client.get(self.register_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'{self.login_url}?next={self.register_url}')

    def test_Logged_Register_Template(self):
        self.client.login(username='admin', password='fatec')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'cadastrar.html')

    def test_register_post_data(self):
        self.client.login(username='admin', password='fatec')
        data= {
            'nome_completo' : 'felipe test',
            'telefone' : '19999768070',
            'email' : 'felipe@fatec.sp.gov.br',
            'observacao' : 'felipe teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Agenda.objects.filter(nome_completo='felipe test').exists())

    def test_register_post_invalid_data(self):
        self.client.login(username='admin', password='fatec')
        data= {
            'nome_completo' : '',
            'telefone' : 'error',
            'email' : 'teste@gmail.com',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'cadastrar.html') # Ajuste no nome do template
        self.assertContains(response, 'Nome completo: Este campo é obrigatório.')
        self.assertContains(response, 'O telefone deve conter apenas')
        self.assertFalse(Agenda.objects.filter(telefone='error').exists())

    def test_register_invalid_phone(self):
        self.client.login(username='admin', password='fatec')   
        data= {
            'nome_completo' : 'felipe test',
            'telefone' : '25615151515151585454',
            'email' : 'test2@fatec.sp.gov.br',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'cadastrar.html')
        self.assertContains(response, 'Telefone: O telefone deve ter entre 10 e 11')
        self.assertFalse(Agenda.objects.filter(nome_completo='jamila test').exists())

    def test_name_with_special_characters(self):
        self.client.login(username='admin', password='fatec')   
        data= {
            'nome_completo' : 'felipe test 3 %@$#',
            'telefone' : '19999768070',
            'email' : 'test@fatec.sp.gov.br',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'cadastrar.html')
        self.assertContains(response, 'Nome completo: O nome completo deve conter apenas letras e espaços.')
        self.assertFalse(Agenda.objects.filter(nome_completo='jamila test 1 %@$#').exists())