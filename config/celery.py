# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Задайте значение переменной окружения для файла настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создайте экземпляр Celery
app = Celery('config')

# Используйте конфигурацию Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте задачи в каждом установленном приложении Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
