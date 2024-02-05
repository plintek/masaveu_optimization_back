from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.rolesManager import rolesManager

from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    passwordComprobation = forms.CharField(
        label='Repetir contraseña', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=rolesManager.getRolesList(),  label="Rol del usuario")

    class Meta:
        model = User
        fields = ('username', 'email', 'groups', 'role')

    def clean_passwordComprobation(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        passwordComprobation = self.cleaned_data.get("passwordComprobation")
        if password and passwordComprobation and password != passwordComprobation:
            raise ValidationError("Las contraseñas no coinciden")
        return passwordComprobation

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Contraseña")
    role = forms.ChoiceField(choices=rolesManager.getRolesList(),  label="Rol del usuario")

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'is_active', 'is_staff',
                  'groups', 'user_permissions', )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'first_name', 'is_staff', 'is_superuser', )
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'role')}),
        ('Personal info', {'fields': ('first_name',)}),

    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'password', 'passwordComprobation', 'role'
                       ),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register to admin site
admin.site.register(User, UserAdmin)
