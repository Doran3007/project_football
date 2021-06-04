# Generated by Django 3.2.3 on 2021-06-04 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_club', '0005_auto_20210604_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='stadium',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='trophy',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]
