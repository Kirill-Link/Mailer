# Generated by Django 5.0 on 2024-01-08 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название фильтра')),
                ('folder', models.CharField(max_length=150, verbose_name='Клиентская папка')),
                ('parent_folder', models.CharField(max_length=150, verbose_name='Родительская папка')),
                ('email', models.CharField(max_length=150, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Фильтр',
                'verbose_name_plural': 'Фильтры',
            },
        ),
    ]
