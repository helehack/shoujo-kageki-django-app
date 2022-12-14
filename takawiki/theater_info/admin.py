from django.contrib import admin
from django.utils.translation import gettext_lazy as _, to_locale
from .models import * # I swear this is not going into production like this, I'm just lazy and may be refactoring.

# Register your models here.

class StageNameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name Information (Please Input in Japanese)', {'fields': ['name', 'reading', 'romaji', 'suffix']}),
        ('Associate Staff Member with Stage Name', {'fields': ['associated_staff_member']})
    ]

admin.site.register(StageName, StageNameAdmin)
admin.site.register(StaffMember)