from django.urls import path
from core.views import login, logout, home, delete, cadastrar, atualizar, listar


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('register_contact/', cadastrar , name='cadastrar_contato'),
    path('show_contact/', listar, name='listar_contato'),
    path('edit_contact/', atualizar, name='atualizar_contato'),
    path('delete_contact/', delete, name='deletar_contato'),
    path('', home,name='home')
]