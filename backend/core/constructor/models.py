from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ConstructedCollection(models.Model):
    name = models.CharField(max_length=255)
    collection_image = models.CharField(
        max_length=255,
        default="https://digital-portfolio.hb.ru-msk.vkcs.cloud/defaultUserAvatar.jpg",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField()
    html_content = models.TextField(blank=True, default="")
    json_data = models.JSONField(blank=True, default=dict)

    class Meta:
        verbose_name = "Коллекция конструктора"
        verbose_name_plural = "Коллекции конструктора"

    def __str__(self):
        return self.name


class UserConstructedCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    constructed_collection = models.ForeignKey(
        ConstructedCollection, on_delete=models.CASCADE
    )
    is_visible = models.BooleanField(default=True, blank=True)

    class Meta:
        unique_together = ["user", "constructed_collection"]
        verbose_name = "Связь коллекция - пользователь"
        verbose_name_plural = "Связи коллекция - пользователь"
