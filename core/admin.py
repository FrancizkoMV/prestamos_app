
from django.contrib import admin
from .models import Cliente, Prestamo, Abono

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id','nombre','identificacion','telefono_1','telefono_2','garantias_firmadas')
    search_fields = ('nombre','identificacion')

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('id','cliente','monto_prestado','tasa_mensual','fecha_prestamo','saldo_capital','saldo_interes','pagado','ultima_actualizacion')
    list_filter = ('pagado', 'fecha_prestamo')
    search_fields = ('cliente__nombre','cliente__identificacion')

@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = ('id','prestamo','monto_abonado','fecha_abono')
    list_filter = ('fecha_abono',)
    search_fields = ('prestamo__cliente__nombre',)
