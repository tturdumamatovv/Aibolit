from django.apps import AppConfig


class MedicineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.medicine'
    def ready(self):
        import apps.medicine.signals