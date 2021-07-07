from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import NewUser

# Register your models here.

admin.site.unregister(Group)

class UserAdminConfig(UserAdmin):
    search_fields=['email','first_name','surname','team', 'job_role']
    list_filter = ('job_role','team','is_admin','is_staff')
    ordering = ('-date_joined',)
    list_display = ('first_name','surname','email','is_admin','is_staff','is_superuser','is_active')
    filter_horizontal=()

    fieldsets = (
        (None, {'fields': ('first_name','surname','email')}),
        ('Permissions', {'fields': ('is_staff','is_admin','is_superuser')}),
        ('Work Details', {'fields': ('team', 'job_role')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','surname','team', 'job_role','email','password1', 'password2', 'is_admin','is_superuser','is_staff')}
         ),
    )



admin.site.register(NewUser)