from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser


class UserAdminConfig(UserAdmin):
    search_fields=['email','first_name','surname','team', 'job_role']
    list_filter = ('job_role','team','groups','is_admin','is_staff')
    ordering = ('-date_joined',)
    list_display = ('first_name','surname','email','is_admin','is_staff','is_superuser','is_active')
    filter_horizontal=()

    fieldsets = (
        (None, {'fields': ('first_name','surname','email')}),
        ('Work Details', {'fields': ('team', 'job_role')}),
        ('Access Permissions', {'fields': ('is_staff','is_admin','is_superuser')}),
        ('Group Permissions', {'fields': ['groups']}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','surname','team', 'job_role','email','password1', 'password2', 'is_admin','is_superuser','is_staff','groups')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)