from django.db import models
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import gettext_lazy as _, to_locale

# custom ENUM tables essentially #
class RoleType(models.Model):
    type = models.CharField(max_length=20) # AUTHOR, CHOREOGRAPHER, COSTUME_DESIGNER, DIRECTOR, COMPOSER, CONDUCTOR, MUSICIAN, ACTOR
    is_onstage_role = models.BooleanField() # add'l fields for named_roles

class GroupType(models.Model):
    type = models.CharField(max_length=20) # GEN_STAFF, BOARD_MEMBER, HANA, TSUKI, YUKI, HOSHI, SORA, OG, GUEST

class WorkType(models.Model):
    type = models.CharField(max_length=20) # REVUE, ONE_ACT_PLAY, TWO_ACT_PLAY, SPECIAL, OTHER

class WorkTextType(models.Model):
    type = models.CharField(max_length=20) # PLOT_SUMMARY, TRIGGER_INFORMATION, TRIVIA

class ProfileTextType(models.Model):
    type = models.CharField(max_length=20) 

class TriggerType(models.Model):
    type = models.CharField(max_length=20) # RAPE, GUNS, SEX, FUN, OTHER

class Genres(models.Model):
    type = models.CharField(max_length=20)

class Venues(models.Model):
    type = models.CharField(max_length=20)

class Geimei(models.Model): # TODO: address The Takigawa Sueko Problem
    role = models.ForeignKey(RoleType)
    geimei = models.CharField(max_length=255)
    geimei_reading = models.CharField(max_length=255)
    geimei_romaji = models.CharField(max_length=255)
    suffix = models.CharField(max_length=10, blank=True) # prefer Chinese over Arabic numerals because these are Japanese Traditional Arts(tm)

    models.UniqueConstraint(fields=['geimei', 'suffix'])

class Works(models.Model): # I wish Sakuhin had a better English equivilant
    work_name = models.CharField(max_length=255)
    work_name_reading = models.CharField(max_length=255)
    work_name_romaji = models.CharField(max_length=255)
    work_type = models.ForeignKey(WorkType)
    work_genre = models.ManyToManyField(Genres, null=True)
    """ will create new NamedRoles entries that will automatically copy everything over from the source work with some reference to original roles... 
    need to be able to display on a chart with previous versions, so need a field for NamedRoles to correlate (parent_character) """
    parent_work = models.ForeignKey('self', null=True)
    trigger_warnings = models.ManyToManyField(TriggerType, null=True)

class WorkTextFields(models.Model):
    work = models.ForeignKey(Works)
    work_text_type = models.ForeignKey(WorkTextType)
    is_in_Japanese = models.BooleanField() # messy temporary solution -- optimally, the canonical data stored on the models is in Japanese, but...
    info = models.TextField()

class NamedRoles(models.Model):
    work = models.ForeignKey(Works)
    role_type = models.ForeignKey(RoleType)

    # if role_type.is_onstage_role:
    is_lead = models.BooleanField(null=True)
    """maybe not the best way to handle this? It's to determine male/female lead but also to help with auto-filling cast lists.
    One could list all of the otokoyaku first if it's a male role assignment. If is_otoko then sort actor list by alphabet then otoko, opposite for musume.
    There are usually more otoko roles and musumeyaku almost never play them unless they're small children. Otokoyaku sometimes play female roles.
    You can still pick whichever actor, but if it doesn't line up with their "usual" role assignment, we usually display it front end. """
    is_otoko = models.BooleanField(null=True) 
    is_in_Japanese = models.BooleanField(null=True) # messy temporary solution -- optimally, the canonical data stored on the models is in Japanese, but...
    character_name = models.CharField(max_length=255, null=True)
    character_name_reading = models.CharField(max_length=255, null=True)
    character_subtitle = models.TextField(null=True)
    parent_character = models.ForeignKey('self', null=True)

class StaffMember(models.Model):
    # add some kind of canonical_name used for URL? For the Takigawas we currently do hatsubutai year but birth year seems more widely applicable... 
    birthdate = models.DateField()
    birthplace = models.CharField(max_length=255)
    honmyou = models.CharField(max_length=255, blank=True)
    canonical_geimei = models.OneToOneField(Geimei)
    associated_geimei = models.ForeignKey(Geimei)

class StaffProfileTextFields(models.Model):
    # Otome stuff or other trivia, CITED, even if not all displayed on front end. From "set list" of translated/able fields with .po strings for content
    profileTextType = models.ForeignKey(ProfileTextType)
    originalText = models.CharField(max_length=255)
    is_official_Hankyu_source = models.BooleanField()
    publicationName = models.CharField(max_length=255)
    publicationAuthor = models.CharField(max_length=255)
    publicationDate = models.DateField(blank=True)
    publicationISBN = models.CharField(max_length=255, blank=True)
    publicationURL = models.CharField(max_length=255, blank=True)
    datetimeAdded = models.DateTimeField() # Apparently it's better to overload save() for this rather than doing auto_now?

class Production(models.Model): # View page
    works = models.ForeignKey(Works)
    associated_groups = models.ForeignKey(GroupType)
    date_start = models.DateField()
    date_end = models.DateField()
    production_blurb = models.TextField()
    
class ProductionRun(models.Model):
    production = models.ForeignKey(Production)
    venue = models.ForeignKey(Venues)
    date_start = models.DateField()
    date_end = models.DateField()

class Performance(models.Model):
    work = models.ForeignKey(Works)
    date_start = models.DateField()
    date_end = models.DateField()

class CastMembers(models.Model):
    performance = models.ForeignKey(Performance)
    geimei = models.ForeignKey(Geimei)
    role = models.ForeignKey(NamedRoles)

class GroupMembership(models.Model):
    geimei = models.ForeignKey(Geimei)
    date_start = models.DateField()
    date_start_production_run = models.ForeignKey(ProductionRun)
    date_end = models.DateField(null=True)
    date_end_production_run = models.ForeignKey(ProductionRun, null=True)
    associated_group = models.ForeignKey(GroupType)