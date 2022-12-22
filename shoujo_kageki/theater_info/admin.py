from django.contrib import admin
from django.utils.translation import gettext_lazy as _, to_locale
from .models import * # I swear this is not going into production like this, I'm just lazy and may be refactoring.

# Register your models here.
 
class GroupMembershipInline(admin.StackedInline):
    model = GroupMembership
    extra = 1

class StageNameAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name Information (Please Input in Japanese)', {'fields': ['name', 'reading', 'romaji', 'suffix']})
    ]
    inlines = [GroupMembershipInline]

class StageNameInline(admin.StackedInline):
    model = StageName
    extra = 0

class StaffProfileTextInline(admin.StackedInline):
    model = StaffProfileTextField
    extra = 1

class StaffMemberAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Vital Statistics (Please Input in Japanese)', {'fields': ['birthdate', 'deathdate', 'birth_country', 'birth_prefecture', 'birth_city', 'given_name', 'given_name_reading', 'given_name_romaji']}),
        ('Display Stage Name', {'fields': ['canonical_stage_name']})
    ]
    inlines = [StaffProfileTextInline, StageNameInline]

class WorkStaffInline(admin.StackedInline):
    model = WorkStaff
    extra = 3

class WorkTextInline(admin.StackedInline):
    model = WorkTextField
    extra = 1

class NamedRoleInline(admin.StackedInline):
    model = NamedRole
    extra = 0

class WorkSceneInline(admin.StackedInline):
    model = WorkScene
    extra = 0

class WorkAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Work Name Information (Japanese Please!)',{'fields':['name','reading','romaji']}),
        ('Other Basic Information',{'fields':['parent_work','work_category','genre','trigger_warnings']}),
        ('Based on...',{'fields':['source_material','source_author','source_material_type']}),
    ]
    inlines = [WorkStaffInline, WorkTextInline, NamedRoleInline, WorkSceneInline]

class ProductionRunInline(admin.StackedInline):
    model = ProductionRun
    extra = 2

class ProductionCastMemberInline(admin.StackedInline):
    model = ProductionCastMember
    extra = 1

class PerformanceInline(admin.StackedInline):
    model = Performance
    extra = 1

class ProductionAdmin(admin.ModelAdmin):
    inlines = [ProductionRunInline, ProductionCastMemberInline]

class PerformanceStaffInline(admin.StackedInline):
    model = PerformanceStaff
    extra = 1
class PerformanceCastMemberInline(admin.StackedInline):
    model = PerformanceCastMember
    extra = 1
class PerformanceAdmin(admin.ModelAdmin):
    inlines = [PerformanceStaffInline, PerformanceCastMemberInline]

class EnumAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

admin.site.register(StageName, StageNameAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Production, ProductionAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register([GroupEnum, TriggerEnum, GenreEnum, VenueEnum, SourceMaterialEnum], EnumAdmin)