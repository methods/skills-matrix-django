# Generated by Django 3.2.4 on 2021-08-17 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0002_usercompetencies'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercompetencies',
            name='job_role_related',
            field=models.BooleanField(default=True),
        ),
    ]
