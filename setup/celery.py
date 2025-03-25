import os
from celery import Celery

# Definir o nome do projeto Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

app = Celery("setup")

# Carregar as configurações do Celery a partir do settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Buscar automaticamente tarefas registradas nos apps do Django
app.autodiscover_tasks()