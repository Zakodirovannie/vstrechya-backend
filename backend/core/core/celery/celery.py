from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "redis://redis-qoovee/1"
app.conf.result_backend = "redis://redis-qoovee/1"
app.autodiscover_tasks()
