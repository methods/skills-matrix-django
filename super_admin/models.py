from django.db import models


class Team(models.Model):
    team_name = models.CharField(max_length=30)


class SkillLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
