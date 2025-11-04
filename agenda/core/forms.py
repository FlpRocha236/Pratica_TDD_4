from django import forms
from django.forms import ModelForm
from core.models import Agenda
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    email = forms.EmailField(label="E-Mail:")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha:")

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")
        if email and password:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if not user:
                raise ValidationError("E-mail ou senha inválidos.")
            cleaned['user'] = user
        return cleaned

class AgendaForm(ModelForm):
    class Meta:
        model = Agenda
        fields = ['nome_completo', 'telefone', 'email', 'observacao']

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
        email = self.cleaned_data.get("email", "")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def clean_observacao(self):
        observacao = self.cleaned_data.get("observacao", "")
        if len(observacao) > 500:
            raise ValidationError("A observação não pode exceder 500 caracteres.")
        return observacao
