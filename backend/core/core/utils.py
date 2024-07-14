import base64
import io

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import encode_uid
from templated_mail.mail import BaseEmailMessage

from core.celery.celery import app
from django.core.cache import cache
from django.conf import settings
import boto3
import uuid

import logging
logger = logging.getLogger('mail')



def delete_cache(key_prefix: str):
    keys_pattern = f"views.decorators.cache.cache_*.{key_prefix}.*.{settings.LANGUAGE_CODE}.{settings.TIME_ZONE}"
    cache.delete_pattern(keys_pattern)


#@app.task
#def send_activation_email_task(context, to):
    #email_message = CustomActivationEmail(None, context)
    #email_message.send(to=to)




@app.task
def upload_image(img, app: str, with_celery=True):
    if with_celery:
        img = io.BytesIO(base64.b64decode(img.decode(encoding="utf-8")))
    key = f"{app}/{uuid.uuid4()}.png"
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3",
        endpoint_url=settings.AWS_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS,
        aws_secret_access_key=settings.AWS_SECRET,
    )
    s3.put_object(Body=img, Bucket="digital-portfolio", Key=key)
    return f"{settings.AWS_URL}{key}"
