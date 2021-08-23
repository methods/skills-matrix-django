from django.contrib import admin
from skills.models import Skill, UserCompetencies
from super_admin.models import SkillLevel

admin.site.register(Skill)
admin.site.register(SkillLevel)
admin.site.register(UserCompetencies)
