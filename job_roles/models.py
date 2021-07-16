from django.db import models
from app.models import Skill, SkillLevel


class Job(models.Model):
    job_title = models.CharField(max_length=50)


class Competency(models.Model):
    job_role_title = models.ForeignKey(Job, on_delete=models.CASCADE)
    job_role_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    job_role_skill_level = models.ForeignKey(SkillLevel, on_delete=models.CASCADE)
