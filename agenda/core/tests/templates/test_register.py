from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import resolve_url as r
from http import HTTPStatus
from core.models import Agenda

class Register_OK_Test(TestCase):
    def setUp(self):
        self.client = Client()
        new_user = User.objects.create(email='admin@fatec.sp.gov.br', username='admin')
        new_user.set_password('fatec')
        new_user.save()
        self.login_url = reverse('login')
        self.register_url = reverse('register_contact')

    def test_Not_Logged_Register_Template(self):
        response = self.client.get(self.register_url)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, f'{self.login_url}?next={self.register_url}')

    def test_Logged_Register_Template(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')

    def test_register_post_data(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        data= {
            'nome_completo' : 'jamila test',
            'telefone' : '19999888802',
            'email' : 'test@fatec.sp.gov.br',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Agenda.objects.filter(nome_completo='jamila test').exists())

    def test_register_post_invalid_data(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')
        data= {
            'nome_completo' : '',
            'telefone' : 'error',
            'email' : 'teste@gmail.com',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')
        self.assertContains(response, 'Nome Completo: Informe o nome completo')
        self.assertContains(response, 'O telefone deve conter apenas')
        self.assertFalse(Agenda.objects.filter(telefone='error').exists())

    def test_register_invalid_phone(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')    
        data= {
            'nome_completo' : 'jamila test',
            'telefone' : '199998888029999999',
            'email' : 'test@fatec.sp.gov.br',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')
        self.assertContains(response, 'Telefone: O telefone deve ter entre 10 e 11')
        self.assertFalse(Agenda.objects.filter(nome_completo='jamila test').exists())

    def test_name_with_special_characters(self):
        self.client.login(email='admin@fatec.sp.gov.br', password='fatec', username='admin')    
        data= {
            'nome_completo' : 'jamila test 1 %@$#',
            'telefone' : '19999888802',
            'email' : 'test@fatec.sp.gov.br',
            'observacao' : 'teste'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')
        self.assertContains(response, 'Nome Completo: O nome completo deve conter apenas letras')
        self.assertFalse(Agenda.objects.filter(nome_completo='jamila test 1 %@$#').exists())
        