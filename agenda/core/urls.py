from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),        
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('agenda/cadastrar/', views.cadastrar, name='cadastrar'),
    path('agenda/atualizar/<int:id>/', views.atualizar, name='atualizar'),
    path('agenda/deletar/<int:id>/', views.deletar, name='delete'),
    path('agenda/listar/', views.listar, name='listar'),
]
