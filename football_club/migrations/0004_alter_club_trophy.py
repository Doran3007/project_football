# Generated by Django 3.2.3 on 2021-06-04 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_club', '0003_auto_20210528_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='trophy',
            field=models.ManyToManyField(blank=True, null=True, to='football_club.Trophy'),
        ),
    ]
