from django.contrib import admin
from django.utils.translation import gettext_lazy as _, to_locale
from .models import * # I swear this is not going into production like this, I'm just lazy and may be refactoring.

# Register your models here.

class StageNameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name Information (Please Input in Japanese)', {'fields': ['name', 'reading', 'romaji', 'suffix']}),
        ('Associate Staff Member with Stage Name', {'fields': ['associated_staff_member']})
    ]

class StaffProfileTextInline(admin.StackedInline):
    model = StaffProfileTextFields
    extra = 1

class StaffMemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Vital Statistics (Please Input in Japanese)', {'fields': ['birthdate', 'deathdate', 'birth_country', 'birth_prefecture', 'birth_city', 'given_name', 'given_name_reading', 'given_name_romaji']}),
        ('Display Stage Name', {'fields': ['canonical_stage_name']})
    ]
    inlines = [StaffProfileTextInline]

class WorkTextInline(admin.StackedInline):
    model = WorkTextField
    extra = 1

class NamedRoleInline(admin.StackedInline):
    model = NamedRole
    extra = 1

class WorkSceneInline(admin.StackedInline):
    model = WorkScene
    extra = 1

class WorkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Work Name Information (Japanese Please!)',{'fields':['name','reading','romaji']}),
        ('Other Basic Information',{'fields':['parent_work','work_category','genre','trigger_warnings']}),
    ]
    inlines = [WorkTextInline, NamedRoleInline, WorkSceneInline]

class ProductionRunInline(admin.StackedInline):
    model = ProductionRun
    extra = 2
class PerformanceInline(admin.StackedInline):
    model = Performance
    extra = 1
class CastMemberInline(admin.StackedInline):
    model = CastMember
    extra = 1

class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionRunInline]

class EnumAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

admin.site.register(StageName, StageNameAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register([RoleEnum, GroupEnum, WorkCategoryEnum, WorkTextEnum, ProfileTextEnum, TriggerEnum, GenreEnum, VenueEnum], EnumAdmin)