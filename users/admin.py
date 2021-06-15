from django.contrib import admin
from .models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from tinymce.widgets import TinyMCE
from django.db import models


from .models import Teacher


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'phone_number', 'first_name',)
    list_filter = ('email', 'phone_number', 'first_name', 'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'phone_number', 'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'first_name', 'second_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        NewUser.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)


class TeacherAdmin(admin.ModelAdmin):
    list_display       = ('teacher', 'full_name', 'phone_number', 'career',)
    list_display_links = ('teacher', 'career',)
    ordering           = ('teacher', 'career',)
    search_fields      = ('teacher', 'career',)

    def full_name(self, obj):
        if obj.teacher.first_name and obj.teacher.second_name:
            return obj.teacher.first_name+" "+obj.teacher.second_name
        else:
            return obj.teacher.first_name
            
    def phone_number(self, obj):
        return str(obj.teacher.phone_number)

    fieldsets = (
        (
            'Teacher', {
                'fields':
                ('teacher', 'image', 'career', 'about',),
            }
        ),
        
    )

    formfield_overrides = {
        models.TextField : {'widget' : TinyMCE}
    }

admin.site.register(Teacher, TeacherAdmin)