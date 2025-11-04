from django.contrib import admin
from .models import Agenda

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "email", "telefone", "observacao")
    search_fields = ("nome_completo", "email")
