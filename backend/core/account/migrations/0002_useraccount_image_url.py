# Generated by Django 5.0.3 on 2024-05-19 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="image_url",
            field=models.CharField(
                default="https://digital-portfolio.hb.ru-msk.vkcs.cloud/defaultUserAvatar.jpg",
                max_length=255,
            ),
        ),
    ]
