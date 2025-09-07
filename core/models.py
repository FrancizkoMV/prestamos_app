
from django.db import models
from datetime import date
from decimal import Decimal

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono_1 = models.CharField(max_length=20)
    telefono_2 = models.CharField(max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField(blank=True, null=True)
    garantias_firmadas = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='prestamos')
    monto_prestado = models.DecimalField(max_digits=15, decimal_places=2)
    tasa_mensual = models.DecimalField(max_digits=5, decimal_places=2, help_text='Porcentaje mensual, ej: 10 para 10%')
    fecha_prestamo = models.DateField(default=date.today)
    saldo_capital = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    saldo_interes = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    pagado = models.BooleanField(default=False)
    ultima_actualizacion = models.DateField(default=date.today)

    class Meta:
        ordering = ['fecha_prestamo', 'id']

    def save(self, *args, **kwargs):
        # Cuando se crea por primera vez, inicializa saldo_capital con monto_prestado si está en cero
        if not self.pk and (self.saldo_capital is None or Decimal(self.saldo_capital) == 0):
            self.saldo_capital = self.monto_prestado
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Préstamo {self.id} a {self.cliente.nombre}"

class Abono(models.Model):
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='abonos')
    monto_abonado = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_abono = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Abono ${self.monto_abonado} al préstamo {self.prestamo_id}"
