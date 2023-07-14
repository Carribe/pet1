from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to="photos/&Y/%m/%d/", verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    belong_to = models.ForeignKey("FilmType", on_delete=models.PROTECT, verbose_name="Категория")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    users = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_page", kwargs={"page_slug": self.slug})

    class Meta:
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"
        ordering = ["time_create", "title"]


class FilmType(models.Model):
    name = models.CharField(max_length=60, db_index=True, verbose_name="Тип плёнки")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_id": self.pk})

    class Meta:
        verbose_name = "Тип плёнки"
        verbose_name_plural = "Типы плёнки"
        ordering = ["id"]
