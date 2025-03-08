from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from profiles.models import  User, StudentProfile, TeacherProfile, AdminProfile, Level


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        * UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields':('is_teacher', 'is_student', 'is_support')
            }
        )
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(AdminProfile)
admin.site.register(Level)