# Generated by Django 3.2.4 on 2021-08-09 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210809_1025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='team',
        ),
    ]
