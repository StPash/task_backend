# Generated by Django 5.0.2 on 2024-03-14 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('author', models.CharField(max_length=255, verbose_name='Автор')),
                ('start', models.DateTimeField(verbose_name='Дата и время старата')),
                ('cost', models.PositiveIntegerField(verbose_name='Стоимость')),
                ('min_group', models.PositiveIntegerField(verbose_name='Макс. кол-во человек в группе')),
                ('max_group', models.PositiveIntegerField(verbose_name='Мин. кол-во человек в группе')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='Ссылка')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.product')),
            ],
        ),
    ]