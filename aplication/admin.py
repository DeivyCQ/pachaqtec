from django.contrib import admin
from .models import Programa, Horario, Unidad, Semana, Cupon, Postulante

# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['nombre_programa','portada','estado']

class HorarioAdmin(admin.ModelAdmin):
    list_display = ['dias','horario','programa']

class UnidadAdmin(admin.ModelAdmin):
    list_display = ['nombre_unidad','programa']

class SemanaAdmin(admin.ModelAdmin):
    list_display = ['nombre_semana','tema','descripcion','unidad']

class PostulanteAdmin(admin.ModelAdmin):
    list_display = ['nombre_postulante','celular','correo','programa']

class CuponAdmin(admin.ModelAdmin):
    list_display = ['codigo_cupon', 'en_uso']


admin.site.register(Programa, ProgramAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Unidad,UnidadAdmin)
admin.site.register(Semana, SemanaAdmin)
admin.site.register(Postulante, PostulanteAdmin)
admin.site.register(Cupon, CuponAdmin)


