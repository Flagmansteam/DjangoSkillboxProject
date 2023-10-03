from typing import Iterable
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse, reverse_lazy


# class Author(models.Model):
#     """
#     Модель Author представляет автора,
#     который пишет статьи в блоге
#
#     Статьи тут: :model:'blogapp.Article'
#     Категории тут: :model:'blogapp.Category'
#     Тэги тут: :model:'blogapp.Tags'
#     Авторы тут: :model:'blogapp.Author'
#     """
#     class Meta:
#         ordering = ["name"]
#         verbose_name_plural = "Авторы"
#         verbose_name = "Автор"
#
#     name = models.CharField(max_length=100, db_index=True)
#     bio = models.TextField(null=False, blank=True, db_index=True )
#
#     def __str__(self):
#         return self.name
#
# class Category(models.Model):
#     """
#     Модель Category представляет категории статей.
#
#     Статьи тут: :model:'blogapp.Article'
#     Тэги тут: :model:'blogapp.Tags'
#     Авторы тут: :model:'blogapp.Author'
#     """
#     class Meta:
#         ordering = ["name"]
#         verbose_name_plural = "Категории"
#         verbose_name = "Категория"
#
#     name = models.CharField(max_length=40, db_index=True)
#
#
#     def __str__(self):
#         return self.name
#
# class Tags(models.Model):
#     """
#     Модель Tags представляет тэг, который можно назначить статье.
#
#     Статьи тут: :model:'blogapp.Article'
#     Категории тут: :model:'blogapp.Category'
#     Авторы тут: :model:'blogapp.Author'
#     """
#     class Meta:
#         ordering = ["name"]
#         verbose_name_plural = "Тэги"
#         verbose_name = "Тэг"
#
#     name = models.CharField(max_length=20, db_index=True)
#
#     def __str__(self):
#         return self.name


class Article(models.Model):
    """
    Модель Article представляет  статью.


    # Категории тут: :model:'blogapp.Category'
    # Авторы тут: :model:'blogapp.Author'
    # Тэги тут: :model:'blogapp.Tags'
    """

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Статьи"
        verbose_name = "Статья"

    title = models.CharField(max_length=200, db_index=True)
    body = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("blogapp:article", kwargs={"pk":self.pk})
