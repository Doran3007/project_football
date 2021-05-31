# Generated by Django 3.1.6 on 2021-05-28 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_club', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trophy',
            name='club',
        ),
        migrations.AddField(
            model_name='club',
            name='trophy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='football_club.trophy'),
            preserve_default=False,
        ),
    ]
