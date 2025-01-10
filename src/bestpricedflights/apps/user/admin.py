from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from bestpricedflights.apps.core.models import City

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[1][1]["fields"] = fieldsets[1][1]["fields"] + ("preferred_origin_city",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "preferred_origin_city":
            kwargs["queryset"] = City.objects.filter(is_origin=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
