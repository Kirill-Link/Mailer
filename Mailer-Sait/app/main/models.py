from django.db import models
from django import forms


class Filters(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название фильтра')
    folder = models.CharField(max_length=150, verbose_name='Клиентская папка')
    parent_folder = models.CharField(max_length=150, verbose_name='Родительская папка')
    email = models.CharField(max_length=150, verbose_name='E-mail')

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def __str__(self):
        return f'Название фильтра: {self.name}'


class AddFilter(forms.ModelForm):
    class Meta:
        model = Filters
        fields = ['name', 'folder', 'parent_folder', 'email']
