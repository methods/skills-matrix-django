# Generated by Django 3.2.4 on 2021-08-09 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_skill_team'),
        ('job_roles', '0003_alter_competency_job_role_skill'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Skill',
        ),
    ]
