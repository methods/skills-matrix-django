from django.db import models
from super_admin.models import Team


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)

