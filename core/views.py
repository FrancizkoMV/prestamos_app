
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from decimal import Decimal
from .models import Cliente, Prestamo, Abono
from .forms import AbonoForm

def dashboard_principal(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'core/dashboard_principal.html', {'clientes': clientes})

def vista_cliente(request):
    # Pantalla simple de demostración
    return render(request, 'core/vista_cliente.html')

def calcular_saldo(prestamo: Prestamo) -> Decimal:
    return (prestamo.saldo_capital or Decimal('0')) + (prestamo.saldo_interes or Decimal('0'))

def _actualizar_intereses(prestamo: Prestamo) -> None:
    """Calcula y acumula intereses desde ultima_actualizacion a hoy."""
    hoy = date.today()
    dias = (hoy - prestamo.ultima_actualizacion).days
    if dias <= 0 or prestamo.pagado:
        prestamo.ultima_actualizacion = hoy
        prestamo.save(update_fields=['ultima_actualizacion'])
        return
    # Interés simple proporcional a días (tasa mensual / 30 * días) sobre saldo de capital
    tasa_diaria = (Decimal(prestamo.tasa_mensual) / Decimal('100')) / Decimal('30')
    intereses_generados = (prestamo.saldo_capital * tasa_diaria) * Decimal(dias)
    # Limitar a mínimo 0
    if intereses_generados < 0:
        intereses_generados = Decimal('0')
    prestamo.saldo_interes += intereses_generados
    prestamo.ultima_actualizacion = hoy
    prestamo.save(update_fields=['saldo_interes', 'ultima_actualizacion'])

def _aplicar_abono(prestamo: Prestamo, monto: Decimal) -> Decimal:
    """Aplica monto a un préstamo: intereses primero, luego capital. Retorna sobrante."""
    if monto <= 0 or prestamo.pagado:
        return monto

    # Actualizar intereses antes de aplicar
    _actualizar_intereses(prestamo)

    usado = Decimal('0')

    # Pagar intereses
    if prestamo.saldo_interes > 0 and monto > 0:
        pago_interes = min(monto, prestamo.saldo_interes)
        prestamo.saldo_interes -= pago_interes
        monto -= pago_interes
        usado += pago_interes

    # Pagar capital
    if prestamo.saldo_capital > 0 and monto > 0:
        pago_capital = min(monto, prestamo.saldo_capital)
        prestamo.saldo_capital -= pago_capital
        monto -= pago_capital
        usado += pago_capital

    # Cerrar si queda en cero
    if prestamo.saldo_capital <= 0 and prestamo.saldo_interes <= 0:
        prestamo.pagado = True

    prestamo.save(update_fields=['saldo_interes', 'saldo_capital', 'pagado'])

    if usado > 0:
        Abono.objects.create(prestamo=prestamo, monto_abonado=usado)

    return monto

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    prestamos_activos = Prestamo.objects.filter(cliente=cliente, pagado=False).order_by('fecha_prestamo', 'id')

    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            monto_restante = Decimal(form.cleaned_data['monto_abonado'])
            # Aplicar abono en orden de antigüedad a todos los préstamos
            for prestamo in prestamos_activos:
                if monto_restante <= 0:
                    break
                monto_restante = _aplicar_abono(prestamo, monto_restante)

            # Si sobra, intentar cerrar los que queden en orden nuevamente
            if monto_restante > 0:
                for prestamo in prestamos_activos:
                    if monto_restante <= 0:
                        break
                    monto_restante = _aplicar_abono(prestamo, monto_restante)

            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = AbonoForm()

    # Actualizar saldos mostrados
    prestamos = list(prestamos_activos)
    for p in prestamos:
        _actualizar_intereses(p)  # para ver intereses al día en la pantalla
        p.saldo_calculado = calcular_saldo(p)

    context = {
        'cliente': cliente,
        'prestamos': prestamos,
        'form': form,
    }
    return render(request, 'core/detalle_cliente.html', context)
