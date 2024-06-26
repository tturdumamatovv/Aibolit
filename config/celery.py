# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите модуль настроек по умолчанию Django для программы Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('project')

# Загрузите настройки из конфигурационного файла Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
