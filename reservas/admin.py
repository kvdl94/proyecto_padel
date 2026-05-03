from django.contrib import admin
from .models import Usuario, Bono, Pista, Reserva


@admin.register(Bono)
class BonoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'creditos', 'creditos_restantes', 'precio', 'fecha_compra')
    list_filter = ('nombre', 'fecha_compra')
    search_fields = ('usuario__username', 'nombre')


admin.site.register(Usuario)
admin.site.register(Pista)
admin.site.register(Reserva)
