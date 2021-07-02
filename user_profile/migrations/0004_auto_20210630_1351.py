# Generated by Django 3.2.4 on 2021-06-30 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_newuser_hashed_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='hashed_password',
        ),
        migrations.AlterField(
            model_name='newuser',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]