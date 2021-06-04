# Generated by Django 3.1.6 on 2021-05-28 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_club', '0002_auto_20210528_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='trophy',
        ),
        migrations.AddField(
            model_name='club',
            name='trophy',
            field=models.ManyToManyField(to='football_club.Trophy'),
        ),
    ]