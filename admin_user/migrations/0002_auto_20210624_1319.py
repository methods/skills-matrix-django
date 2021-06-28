# Generated by Django 3.2.4 on 2021-06-24 13:19

from django.db import migrations


def add_sample_jobs(apps, schema_editor):
    Job = apps.get_model('admin_user', 'Job')
    jobs = ['Junior Developer', 'Mid Developer', 'Senior Developer', 'Lead Developer', 'Head of Development',
            'User Researcher', 'Delivery Manager']
    for job in jobs:
        j = Job(job_title=job)
        j.save(force_insert=True)


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_sample_jobs)
    ]