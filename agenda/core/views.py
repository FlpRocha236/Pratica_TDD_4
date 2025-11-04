from django.shortcuts import render, redirect
from core.forms import LoginForm, AgendaForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from core.models import Agenda

def login(request):
    if request.user.id is not None:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.user)
            return redirect("home")
        context = {'acesso_negado': True}
        return render(request, 'login.html', {'form':form})
    return render(request, 'login.html', {'form':LoginForm()})

        
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return render(request, 'logout.html')
    return redirect("home")


@login_required
def home(request):
    context = {}
    return render(request, 'index.html', context)

@login_required
def register_contact(request):
    context = {}
    if request.method == "POST":
        nome = request.POST.get('nome_completo')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        
        data = {
            'nome_completo': nome,
            'telefone': telefone,
            'email': email,
            'observacao': observacao
        }

        form = AgendaForm(data)
        if form.is_valid():
            form.save()
            context = {'success': True, 'data': form}
            return redirect("home")
        else:
            context = {'error': True, 'form': form}
            return render(request, 'register_contact.html', context)
    return render(request, 'register_contact.html', context)

@login_required
def show_contact(request):
    contacts = Agenda.objects.all().order_by('nome_completo')
    context = {'contacts':contacts}
    return render(request, 'show_contact.html', context)

@login_required
def edit_contact(request):
    context = {}
    contacts = Agenda.objects.all().order_by('id')
    context = {'contacts':contacts}
    if request.method == "POST":
        id = request.POST.get('id')
        nome = request.POST.get('nome_completo')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        observacao = request.POST.get('observacao')
        if not id:
            context = {'error': True, 'errors': "ID nao encontrado."}
            return render(request, 'edit_contact.html', context)
        if not Agenda.objects.filter(id=id).exists():
            context = {'error': True, 'errors': "Contato nao encontrado."}
            return render(request, 'edit_contact.html', context)
        data = {
            'nome_completo': nome,
            'telefone': telefone,
            'email': email,
            'observacao': observacao
        }

        form = AgendaForm(data)
        if form.is_valid():
            agenda = Agenda.objects.get(id=id)
            agenda.nome_completo = nome
            agenda.telefone = telefone
            agenda.email = email
            agenda.observacao = observacao
            agenda.save()
            context = {'success': True, 'data': form}
            return redirect("home")
        else:
            context = {'error': True, 'form': form, 'contacts':contacts}
            return render(request, 'edit_contact.html', context)
    if request.method == "GET":
        context = {'contacts':contacts}
        return render(request, 'edit_contact.html', context)
    return render(request, 'edit_contact.html', context)

@login_required
def delete_contact(request):
    context = {}
    if request.method == "GET":
        contacts = Agenda.objects.all().order_by('id')
        context = {'contacts':contacts}
        return render(request, 'delete_contact.html', context)
    if request.method == "POST":
        id = request.POST.get('id')
        if not id:
            context = {'error': True, 'errors': "ID não encontrado."}
            return render(request, 'delete_contact.html', context)
        if not Agenda.objects.filter(id=id).exists():
            context = {'error': True, 'errors': "Contato não encontrado."}
            return render(request, 'delete_contact.html', context)
        agenda = Agenda.objects.get(id=id)
        agenda.delete()
        context = {'success': True}
        return redirect("home")
    return render(request, 'delete_contact.html', context)