from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.forms import LoginForm, AgendaForm
from core.models import Agenda
from django.shortcuts import render, redirect, get_object_or_404

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request.POST or None)
    context = {"form": form}
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("home")
    return render(request, "login.html", context)

@login_required(login_url="login")
def logout_view(request):
    auth_logout(request)
    return render(request, "logout.html")

@login_required(login_url="login")
def home(request):
    contacts = Agenda.objects.all()
    return render(request, "index.html", {"contacts": contacts})

@login_required(login_url="login")
def cadastrar(request):
    form = AgendaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "cadastrar.html", {"form": form})

@login_required(login_url="login")
def atualizar(request, id):
    agenda = get_object_or_404(Agenda, id=id)
    form = AgendaForm(request.POST or None, instance=agenda)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "atualizar.html", {"form" : form})

@login_required(login_url="login")
def deletar(request, id):
    agenda = get_object_or_404(Agenda, id=id)
    if request.method == "POST":
        agenda.delete()
        return redirect("home")
    return render(request, "delete.html", {"agenda": agenda})

@login_required(login_url="login")
def listar(request):
    contacts = Agenda.objects.all()
    return render(request, "listar.html", {"contacts": contacts})