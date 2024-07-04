from django.apps import AppConfig


class CeleryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.celery"
    verbose_name = "Celery"
