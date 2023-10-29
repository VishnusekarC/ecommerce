from django.contrib import admin
from .models import *


class StateAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
