from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    fieldsets = (('Personal Details', {
            'classes': ('wide',),
            'fields': ('full_name', 'mobile','email', 'password')}
        ),
        ('Permission', {
            'fields' : ('active', 'admin', 'staff')
        })
        )
    # add form in admin site
    add_form = UserAdminCreationForm
    add_fieldsets = (
        ('Personal Details', {
            'classes': ('wide',),
            'fields': ('full_name', 'mobile','email')}
        ),
        ('Password Details', {
            'classes': ('wide',),
            'fields': ('password1', 'password2')}
        ),
    )
    filter_horizontal = []
    ordering = ['full_name']
    list_display = ['email', 'full_name']
    list_filter = ['admin']
    search_fields = ['full_name', 'email', 'mobile']

# Register your models here.
admin.site.register(User, UserAdmin)
