# Generated by Django 3.2.4 on 2021-07-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=400)),
                ('skill_type', models.CharField(choices=[('career_skill', 'Career skill'), ('general_skill', 'General skill')], max_length=13)),
            ],
        ),
    ]
