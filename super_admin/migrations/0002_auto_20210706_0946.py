# Generated by Django 3.2.4 on 2021-07-06 09:46

from django.db import migrations
def add_sample_teams(apps, schema_editor):
    Team = apps.get_model('super_admin', 'Team')
    teams = ['OPC', 'Technology', 'Delivery', 'User Experience']
    for team in teams:
        t = Team(team_name=team)
        t.save()
class Migration(migrations.Migration):
    dependencies = [
        ('super_admin', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_sample_teams)
    ]