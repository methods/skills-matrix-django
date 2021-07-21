from django.contrib import admin
from .models import Skill
from super_admin.models import SkillLevel

# Register your models here.

admin.site.register(Skill)
admin.site.register(SkillLevel)