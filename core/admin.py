from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Exam, Session, SessionNote

'''
    Custom User Admin
'''
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'email_frequency')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('avatar', 'email_frequency')}),
    )

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Exam)
admin.site.register(Session)
admin.site.register(SessionNote)