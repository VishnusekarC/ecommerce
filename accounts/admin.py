from django.contrib import admin
from .models import *




class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_admin', 'is_superuser')
    list_filter = ('is_active', 'is_admin', 'is_superuser')
    # readonly_fields = ('created_at', 'updated_at')

class CustomUserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'username')
    readonly_fields = ('created_at', 'updated_at')

class CustomUserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'phone', 'pin_code', 'state', 'city')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUserDetail, CustomUserDetailAdmin)
admin.site.register(CustomUserAddress, CustomUserAddressAdmin)
