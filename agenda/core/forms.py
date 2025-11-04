from django import forms
from django.forms import ModelForm
from core.models import Agenda
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'senha': forms.PasswordInput(attrs={'class': 'form-control'}),
    }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("E-mail não cadastrado ou senha incorreta.", code='invalid_login')

            user = authenticate(username=user_obj.username, password=senha) 
            
            if user is None:
                raise forms.ValidationError("E-mail não cadastrado ou senha incorreta.", code='invalid_login')
            
            self.user = user          
        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)

class AgendaForm(ModelForm):
    class Meta:
        model = Agenda
        fields = ['nome_completo', 'telefone', 'email', 'observacao']

        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nome_completo(self):
        nome = self.cleaned_data.get("nome_completo", "")
        if not all(c.isalpha() or c.isspace() for c in nome):
            raise ValidationError("O nome completo deve conter apenas letras e espaços.")
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get("telefone", "")
        if not telefone.isdigit():
            raise ValidationError("O telefone deve conter apenas números.")
        if len(telefone) < 10 or len(telefone) > 11:
            raise ValidationError("O telefone deve ter entre 10 e 11 dígitos.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith('@fatec.sp.gov.br'): 
            raise forms.ValidationError('Informe seu e-mail institucional.')
        return email

    def clean_observacao(self):
        observacao = self.cleaned_data.get("observacao", "")
        if len(observacao) > 500:
            raise ValidationError("A observação não pode exceder 500 caracteres.")
        return observacao