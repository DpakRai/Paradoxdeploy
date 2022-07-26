from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import UserProfile


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
    list_display = ('email', 'is_admin', 'is_active','username')
    list_filter = ('email', 'is_admin', 'is_active','username')
    fieldsets = (
        (None, {'fields': ('email', 'password','username','related_admin')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin')}),
        ('Personal info', {'fields': ('first_name', 'last_name','ip_address','country','age','avatar')}),
        ('Subscription', {'fields': ('subscription','subscribed_date',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)

class CustomUserActivity(admin.ModelAdmin):
    list_display = ('user', 'created_at')

admin.site.register(UserProfile, CustomUserAdmin)
admin.site.register(Subscription)
admin.site.register(Review)
admin.site.register(UserActivity, CustomUserActivity)