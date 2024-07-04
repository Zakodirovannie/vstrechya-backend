from django.db import models

from account.models import UserAccount
from museum.models import Museum


class Collection(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

    def __str__(self):
        return self.name


class UserCollection(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user_id", "collection_id"]
        verbose_name = "Коллекция пользователей"
        verbose_name_plural = "Коллекции пользователей"


class MuseumCollection(models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Коллекция музея"
        verbose_name_plural = "Коллекции музеев"

    def __str__(self):
        return str(self.museum)


class MuseumCollectionUser(models.Model):
    collection = models.ForeignKey(MuseumCollection, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    can_add_item = models.BooleanField(default=False)
    can_delete_item = models.BooleanField(default=False)
    can_change_item = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Редактор коллекций музеев"
        verbose_name_plural = "Редакторы коллекций музеев"

    def __str__(self):
        return f"{self.collection} | {self.user}"


class CollectionItem(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Изображение коллекций"
        verbose_name_plural = "Изображения коллекций"
