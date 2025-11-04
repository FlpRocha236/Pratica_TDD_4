from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from core.models import Agenda

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        labels = {
            'email': 'E-Mail:',
            'password': 'Senha:',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail institucional'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control',
                                                   'placeholder':'Digite sua senha'}),
        }
        error_messages = {
            'email': {
                'required': ("Informe o e-mail."),
            },
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@fatec.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Usuário com esse e-mail não encontrado.")

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise ValidationError("Senha incorreta para o e-mail informado.")

            self.user = user

class AgendaForm(ModelForm):
    class Meta:
        model = Agenda
        fields = ('nome_completo', 'telefone', 'email', 'observacao')
        labels = {
            'nome_completo': 'Nome Completo:',
            'telefone': 'Telefone:',
            'email': 'E-Mail:',
            'observacao': 'Observação:',
        }
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder':'Digite seu nome completo'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder':'Digite seu telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                             'placeholder':'Digite seu e-mail institucional'}),
            'observacao': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder':'Digite uma observação'}),
        }
        error_messages = {
            'nome_completo': {
                'required': ("Informe o nome completo."),
            },
            'telefone': {
                'required': ("Informe o telefone."),
            },
            'email': {
                'required': ("Informe o e-mail."),
            },
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@fatec.sp.gov.br'):
            raise ValidationError('Informe seu e-mail institucional.')
        return self.cleaned_data['email']
    
    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if not telefone.isdigit():
            raise ValidationError('O telefone deve conter apenas números.')
        if len(telefone) < 10 or len(telefone) > 11:
            raise ValidationError('O telefone deve ter entre 10 e 11 dígitos.')
        return telefone
    
    def clean_nome_completo(self):
        nome_completo = self.cleaned_data['nome_completo']
        if not nome_completo.replace(" ", "").isalpha():
            raise ValidationError('O nome completo deve conter apenas letras e espaços.')
        return nome_completo