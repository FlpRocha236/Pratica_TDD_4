from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import Agenda
from core.forms import AgendaForm, LoginForm
from django.urls import reverse 

User = get_user_model()



class AgendaModelTest(TestCase):
    def setUp(self):
        self.agenda = Agenda.objects.create(
            nome_completo="João da Silva",
            telefone="19999998888",
            email="joao.silva@example.com",
            observacao="Cliente importante."
        )

    def test_agenda_criada_com_sucesso(self):
        self.assertEqual(self.agenda.nome_completo, "João da Silva")
        self.assertEqual(self.agenda.telefone, "19999998888")
        self.assertEqual(self.agenda.email, "joao.silva@example.com")
        self.assertEqual(self.agenda.observacao, "Cliente importante.")

    def test_str_retorna_nome_e_email(self):
        self.assertEqual(str(self.agenda), "João da Silva - joao.silva@example.com")



class AgendaFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nome_completo': 'Felipe Rocha',
            'telefone': '19999768070',
            'email': 'felipe@fatec.sp.gov.br',
            'observacao': 'Teste'
        }

    def test_form_has_fields(self):
        form = AgendaForm()
        expected_fields = ['nome_completo', 'telefone', 'email', 'observacao']
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_valid_form(self):
        form = AgendaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_nome_completo_obrigatorio(self):
        data = self.valid_data.copy()
        data['nome_completo'] = ''
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome_completo', form.errors)

    def test_nome_completo_sem_numeros(self):
        data = self.valid_data.copy()
        data['nome_completo'] = 'Felipe123'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('O nome completo deve conter apenas letras e espaços.', form.errors['nome_completo'])

    def test_telefone_somente_numeros(self):
        data = self.valid_data.copy()
        data['telefone'] = '1999ABCD'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('O telefone deve conter apenas números.', form.errors['telefone'])

    def test_telefone_com_digitos_invalidos(self):
        data = self.valid_data.copy()
        data['telefone'] = '123'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('O telefone deve ter entre 10 e 11 dígitos.', form.errors['telefone'])

    def test_email_institucional(self):
        data = self.valid_data.copy()
        data['email'] = 'teste@gmail.com'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('Informe seu e-mail institucional.', form.errors['email'])



class LoginFormTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',
            email='orlando@fatec.sp.gov.br',
            password='senha123'
        )

    def make_validated_form(self, **kwargs):
        data = {'email': 'orlando@fatec.sp.gov.br', 'senha': 'senha123'}
        data.update(kwargs)
        form = LoginForm(data=data)
        form.is_valid()
        return form

    def test_form_has_fields(self):
        form = LoginForm()
        expected_fields = ['email', 'senha']
        self.assertSequenceEqual(list(form.fields), expected_fields)


    def test_email_obrigatorio(self):
        form = self.make_validated_form(email='')
        self.assertIn('email', form.errors)

    def test_email_inexistente(self):
        form = self.make_validated_form(email='nao@fatec.sp.gov.br')
        self.assertIn('__all__', form.errors) 
        self.assertIn('E-mail não cadastrado ou senha incorreta.', form.errors['__all__'])

    def test_senha_errada(self):
        form = self.make_validated_form(senha='senhaerrada')
        self.assertIn('__all__', form.errors) 
        self.assertIn('E-mail não cadastrado ou senha incorreta.', form.errors['__all__'])

    def test_autentica_usuario_valido(self):
        form = self.make_validated_form()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

class AgendaIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin',  
            email='admin@fatec.sp.gov.br', 
            password='fatec'
        )
        
        self.client = Client()
        
       
        self.client.login(
            username='admin', 
            password='fatec'
        )

        self.contato = Agenda.objects.create(
            nome_completo='Fulano Teste',
            telefone='19999998888',
            email='fulano@fatec.sp.gov.br'
        )

    def test_cadastrar_contato(self):
        data = {
            'nome_completo': 'Ciclano',
            'telefone': '19999997777',
            'email': 'ciclano@fatec.sp.gov.br',
            'observacao': 'Novo contato'
        }
    
        response = self.client.post(reverse('cadastrar'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Agenda.objects.filter(nome_completo='Ciclano').exists())

    def test_atualizar_contato(self):
        data = {
            'nome_completo': 'Fulano Atualizado',
            'telefone': self.contato.telefone,
            'email': self.contato.email,
            'observacao': self.contato.observacao
        }

        url = reverse('atualizar_contato', kwargs={'id': self.contato.id})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.contato.refresh_from_db()
        self.assertEqual(self.contato.nome_completo, 'Fulano Atualizado')

    def test_deletar_contato(self):
        url = reverse('delete', kwargs={'id': self.contato.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Agenda.objects.filter(id=self.contato.id).exists())

    def test_listar_contatos(self):
        response = self.client.get(reverse('listar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contato.nome_completo)