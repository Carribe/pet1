# Generated by Django 4.2.3 on 2023-07-06 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=60, verbose_name='Тип плёнки')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тип плёнки',
                'verbose_name_plural': 'Типы плёнки',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('content', models.TextField(blank=True, verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='photos/&Y/%m/%d/', verbose_name='Фото')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
                ('belong_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pages.filmtype', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Статью',
                'verbose_name_plural': 'Статьи',
                'ordering': ['time_create', 'title'],
            },
        ),
    ]
