from django.db import models
from account.models import UserAccount


class Museum(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    short_name = models.CharField(null=True, max_length=20, verbose_name="Аббревиатура")
    image_url = models.CharField(
        max_length=255,
        default="https://digital-portfolio.hb.ru-msk.vkcs.cloud/defaultMuseumAvatar.png",
    )
    description = models.TextField(null=True, max_length=500, verbose_name="Описание")
    address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Адрес"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Музей"
        verbose_name_plural = "Музеи"

    def __str__(self):
        return self.name


class MuseumUser(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE, verbose_name="Музей")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Присоеденился")
    position = models.CharField(
        max_length=30, default="Сотрудник", verbose_name="Должность"
    )
    is_owner = models.BooleanField(default=False)
    can_change_name = models.BooleanField(default=False)
    can_change_short_name = models.BooleanField(default=False)
    can_change_description = models.BooleanField(default=False)
    can_change_address = models.BooleanField(default=False)
    can_add_users = models.BooleanField(default=False)
    can_delete_users = models.BooleanField(default=False)
    can_change_user_permissions = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Сотрудник музея"
        verbose_name_plural = "Сотрудники музеев"
        unique_together = ("user", "museum")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.user.email}"
