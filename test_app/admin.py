from django.contrib import admin
from .models import Custom_User,Personal_Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField


class UserForm(BaseUserCreationForm):
    """
    Form for new user create in System
    """
    class Meta:
        model = Custom_User
        fields = ('username','email',)
        field_classes = {'username': UsernameField}
        

class UserAdmin(BaseUserAdmin):
    add_form = UserForm
    list_display = ('id', 'username', 'email', 'first_name', 'middle_name', 'last_name', 'is_staff','is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'middle_name', 'last_name', 'email')
    ordering = ('username',)


admin.site.register(Personal_Profile)
admin.site.register(Custom_User)