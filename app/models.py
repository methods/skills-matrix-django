from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, blank=True)
    skill_type = models.CharField(choices=[('career_skill', 'Career skill'), ('general_skill', 'General skill')],
                                  max_length=13)


class SkillLevel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
