
# Proyecto Django - Préstamos (versión corregida)

Instrucciones rápidas:

1. Crea/activa tu entorno virtual e instala Django 5.x:
   ```bash
   pip install django==5.0.6
   ```
2. Entra a la carpeta del proyecto (donde está `manage.py`).
3. Ejecuta migraciones y levanta el servidor:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # opcional
   python manage.py runserver
   ```

Entradas útiles:
- `/admin/` para admin de Django.
- `/dashboard/` para ver clientes y entrar al detalle.
- `/cliente/<id>/` para detalle.
