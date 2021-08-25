from django.db import models
from super_admin.models import Team, SkillLevel
from user_management.models import NewUser


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)


class UserCompetencies(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_level = models.ForeignKey(SkillLevel, on_delete=models.CASCADE)
    job_role_related = models.BooleanField(default=True)
