from django.db import models
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import gettext_lazy as _, to_locale
from django.contrib.auth.models import User

# custom ENUM tables essentially #
class RoleEnum(models.Model):
    enum = models.CharField(max_length=20) # AUTHOR, CHOREOGRAPHER, COSTUME_DESIGNER, DIRECTOR, COMPOSER, CONDUCTOR, MUSICIAN, ACTOR
    is_onstage_role = models.BooleanField() # add'l fields for named_roles

class GroupEnum(models.Model):
    enum = models.CharField(max_length=20) # GEN_STAFF, BOARD_MEMBER, HANA, TSUKI, YUKI, HOSHI, SORA, SENKA, OG, GUEST

class WorkEnum(models.Model): # this needs a better name WorkTypeEnum? I'm trying to stay away from "type". Ugh.
    enum = models.CharField(max_length=20) # REVUE, ONE_ACT_PLAY, TWO_ACT_PLAY, SPECIAL, OTHER

class WorkTextEnum(models.Model):
    enum = models.CharField(max_length=20) # PLOT_SUMMARY, TRIGGER_INFORMATION, TRIVIA

class ProfileTextEnum(models.Model):
    enum = models.CharField(max_length=20) # Otome stuff (NAME_ORIGIN, FAV_COLOR, FAV_FLOWER, HOBBIES) + TRIVIA section at bottom of page

class TriggerEnum(models.Model):
    enum = models.CharField(max_length=20) # RAPE, NONCON, GUNS, OTHER, etc

class GenreEnum(models.Model):
    enum = models.CharField(max_length=20) # LATIN, CLASSIC, etc

class VenueEnum(models.Model):
    enum = models.CharField(max_length=20) # 宝塚大劇場, 東京宝塚劇場

class ChangelogInfo(models.Model): 
    pass
    """ I'm not sure how much of this is already handled internally in admin, but I definitely want to associate additional fields with it.
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    publication_name = models.CharField(max_length=255)
    publication_author = models.CharField(max_length=255, blank=True)
    publication_year = models.DateField(blank=True)
    publication_ISBN_ASIN = models.CharField(max_length=255, blank=True)
    publication_URL = models.CharField(max_length=255, blank=True)
    time_updated = models.DateTimeField()
    fields_updated = no idea how to manage this one """

class StageName(models.Model):
    name = models.CharField(max_length=255)
    reading = models.CharField(max_length=255)
    romaji = models.CharField(max_length=255)
    suffix = models.CharField(max_length=10, blank=True) # prefer Chinese over Arabic numerals because these are Japanese Traditional Arts(tm)
    associated_staff_member = models.ForeignKey('theater_info.StaffMember', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['romaji', 'suffix'], name='Combination of romaji reading and suffix should be unique as it will be used as a URL slug.') ]

class Work(models.Model): # I wish Sakuhin had a better English equivilant
    name = models.CharField(max_length=255)
    reading = models.CharField(max_length=255)
    romaji = models.CharField(max_length=255)
    enum = models.ForeignKey(WorkEnum, on_delete=models.PROTECT)
    genre = models.ManyToManyField(GenreEnum)
    """ will create new NamedRole entries that will automatically copy everything over from the source work with some reference to original roles... 
    need to be able to display on a chart with previous versions, so need a field for NamedRole to correlate (parent_character) """
    parent_work = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    trigger_warnings = models.ManyToManyField(TriggerEnum)

class WorkTextField(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    text_enum = models.ForeignKey(WorkTextEnum, on_delete=models.PROTECT)
    is_in_Japanese = models.BooleanField() # messy temporary solution -- optimally, the canonical data stored on the models is in Japanese, but...
    text = models.TextField()

class NamedRole(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    role_enum = models.ForeignKey(RoleEnum, on_delete=models.PROTECT)

    # if role_enum.is_onstage_role:
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
    parent_character = models.ForeignKey('self', on_delete=models.PROTECT, null=True)

class StaffMember(models.Model):
    birthdate = models.DateField(null=True)
    birth_country = models.CharField(max_length=255, blank=True, default='日本国')
    birth_prefecture = models.CharField(max_length=255, blank=True)
    birth_city = models.CharField(max_length=255, blank=True)
    given_name = models.CharField(max_length=255, blank=True)
    given_name_romaji = models.CharField(max_length=255, blank=True)
    canonical_stage_name = models.OneToOneField(StageName, on_delete=models.PROTECT)

class StaffProfileTextFields(models.Model):
    associated_staff_member = models.ForeignKey(StaffMember, on_delete=models.PROTECT)
    # Otome stuff or other trivia, CITED, even if not all displayed on front end. From "set list" of translated/able fields with .po strings for content
    profile_text_enum = models.ForeignKey(ProfileTextEnum, on_delete=models.PROTECT)
    original_text = models.CharField(max_length=255)
    is_official_Hankyu_source = models.BooleanField()

class Production(models.Model): # View page
    works = models.ManyToManyField(Work)
    associated_groups = models.ManyToManyField(GroupEnum)
    date_start = models.DateField()
    date_end = models.DateField()
    production_blurb = models.TextField()
    
class ProductionRun(models.Model):
    production = models.ForeignKey(Production, on_delete=models.PROTECT)
    venue = models.ForeignKey(VenueEnum, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField()

class Performance(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)
    tour_venue = models.CharField(max_length=255, null=True, blank=True) # for encapsulating national tour information
    associated_production_run = models.ForeignKey(ProductionRun, on_delete=models.PROTECT)

class CastMember(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    role = models.ForeignKey(NamedRole, on_delete=models.PROTECT)

class GroupMembership(models.Model):
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_start_performance = models.ForeignKey(Performance, on_delete=models.PROTECT, related_name='group_join') # if we don't know this info, there will be a dummy Show/Production/ProductionRun/Performance
    date_end = models.DateField(null=True)
    date_end_performance = models.ForeignKey(Performance, on_delete=models.PROTECT, null=True, related_name='group_depart')
    associated_group = models.ForeignKey(GroupEnum, on_delete=models.PROTECT)
    gender_role = models.CharField( max_length=2, choices=[('OY', 'otokoyaku'), ('MY', 'musumeyaku'), ('BT', 'both'), ('NA', 'not applicable'),], default='NA' )

""" TODO: 
 - Photos -- headshots for staff members and chirashi/header for exhibitions. Look into library options. Easy Thumbnails? 
 - Glossary? Might be a separate app; pain in the ass to localize. Situation normal.
 - OH YEAH LOCALIZATION associated translation tables by domain; locale-slug-associated field (enums should be useful for this)-text?
"""