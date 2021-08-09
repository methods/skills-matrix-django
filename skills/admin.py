from django.contrib import admin
from skills.models import Skill
from super_admin.models import SkillLevel

admin.site.register(Skill)
admin.site.register(SkillLevel)
