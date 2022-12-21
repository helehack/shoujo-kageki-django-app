from django.db import models
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Language(models.TextChoices):
    ENGLISH = 'en-US','English'
    JAPANESE = 'ja-JP','日本語'

# custom ENUM tables essentially #
class GroupEnum(models.Model):
    enum = models.CharField(max_length=20) # GEN_STAFF, BOARD_MEMBER, HANA, TSUKI, YUKI, HOSHI, SORA, SENKA, OG, GUEST

    def __str__(self):
        return self.enum

class TriggerEnum(models.Model):
    enum = models.CharField(max_length=20) # RAPE, NONCON, GUNS, OTHER, etc

    def __str__(self):
        return self.enum

class GenreEnum(models.Model):
    enum = models.CharField(max_length=20) # LATIN, CLASSIC, etc

    def __str__(self):
        return self.enum

class VenueEnum(models.Model):
    enum = models.CharField(max_length=20) # 宝塚大劇場, 東京宝塚劇場

    def __str__(self):
        return self.enum

class SourceMaterialEnum(models.Model):
    enum = models.CharField(max_length=20)

    def __str__(self):
        return self.enum

class ChangelogInfo(models.Model): 
    pass
    """ 
    TODO: Look at some of the jazzband projects for this sort of thing, such as django-simple-history and django-auditlog.
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
    
    def __str__(self):
        return (self.name + " " + self.romaji)

class StaffMember(models.Model):
    birthdate = models.DateField(null=True)
    deathdate = models.DateField(null=True, blank=True)
    birth_country = models.CharField(max_length=255, blank=True, default='日本国')
    birth_prefecture = models.CharField(max_length=255, blank=True)
    birth_city = models.CharField(max_length=255, blank=True)
    given_name = models.CharField(max_length=255, blank=True)
    given_name_reading = models.CharField(max_length=255, blank=True)
    given_name_romaji = models.CharField(max_length=255, blank=True)
    canonical_stage_name = models.OneToOneField(StageName, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.canonical_stage_name) + " (" + self.given_name + " " + self.given_name_romaji + ")" 

class StaffProfileTextFields(models.Model):
    associated_staff_member = models.ForeignKey(StaffMember, on_delete=models.PROTECT)
    profile_text_type = models.CharField(max_length=15, choices=[
        ('blood_type','Blood Type'),
        ('nickname','Nickname'),
        ('flower','Favorite Flower'),
        ('food','Favorite Food'),
        ('color','Favorite Color'),
        ('hobby','Hobby'),
        ('collection','Collection'),
        ('talent','Special Talent'),
        ('name_origin','Origin of Stage Name'),
        ('role','Favorite Role'),
        ('like_to_play','Would Like to Try Playing'),
        ('trivia','Trivia'),
        ('social','Social Media/Website'),
        ('other','Other'),
    ], default='other')
    original_text = models.CharField(max_length=255)
    is_in_Japanese = models.BooleanField(default='False')
    is_current_data = models.BooleanField(default='True')
    source_material = models.CharField(max_length=255, default='Unknown')
    source_year = models.CharField(max_length=4, default='None')

    def __str__(self):
        return self.profile_text_type

class Work(models.Model): # I wish Sakuhin had a better English equivilant
    name = models.CharField(max_length=255)
    reading = models.CharField(max_length=255)
    romaji = models.CharField(max_length=255)
    work_category = models.CharField(max_length=15, choices=[
        ('one_act', 'One-Act Play'),
        ('two_act', 'Two-Act Play'),
        ('revue', 'Revue'),
        ('dinner_show', 'Dinner Show'),
        ('music_salon', 'Music Salon'),
        ('buyoukai', 'Buyoukai'),
        ('tmp_tca', 'TMP/TCA/Mirror Ball Special'),
        ('other_special', 'Other Special'),
        ('other', 'Other')
    ])
    genre = models.ManyToManyField(GenreEnum, blank=True)
    # nihonmono timeline fields?
    """ will create new NamedRole entries that will automatically copy everything over from the source work with some reference to original roles... 
    need to be able to display on a chart with previous versions, so need a field for NamedRole to correlate (parent_character) """
    trigger_warnings = models.ManyToManyField(TriggerEnum, blank=True)
    parent_work = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    source_material = models.CharField(max_length=255, blank=True)
    source_author = models.CharField(max_length=255, blank=True)
    source_material_type = models.ManyToManyField(SourceMaterialEnum, blank=True)

    def __str__(self):
        return self.name + " " + self.romaji

class WorkStaff(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    work_staff_role = models.CharField(max_length=15, choices=[
        ('writer', 'Writer'), ('choreographer', 'Choreographer'),('composer','Composer')
    ])
    staff_stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)

class WorkTextField(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    language = models.CharField(max_length=5, choices=Language.choices)
    text_type = models.CharField(max_length=15, choices=[
        ('plot_summary','Plot Summary'),
        ('trigger_info','Additional Trigger Information'),
        ('trivia','Trivia'),
    ])
    text = models.TextField()

class NamedRole(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    is_lead = models.BooleanField(null=True)
    is_otokoyaku_role = models.BooleanField(null=True) 
    jp_character_name = models.CharField(max_length=255, blank=True)
    character_name_reading = models.CharField(max_length=255, blank=True)
    character_name_romaji = models.CharField(max_length=255)
    character_subtitle = models.TextField(null=True, blank=True)
    parent_character = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        if(self.jp_character_name):
            return self.jp_character_name + " " + self.character_name_romaji
        
        return self.character_name_romaji

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

class PerformanceCastMember(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    role = models.ForeignKey(NamedRole, on_delete=models.PROTECT)

class PerformanceStaff(models.Model):
    production_run = models.ForeignKey(Performance, on_delete=models.PROTECT)
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    performance_staff_role = models.CharField(max_length=15, choices=[('director','Director'),('conductor','Conductor'),])

class WorkScene(models.Model):
    associated_work = models.ForeignKey(Work, on_delete=models.PROTECT)
    associated_work_staff = models.ManyToManyField(WorkStaff)
    associated_named_roles = models.ManyToManyField(NamedRole)
    parent_scene = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    en_title = models.CharField(max_length=255, blank=True)
    jp_title = models.CharField(max_length=255, blank=True)
    en_description = models.TextField(blank=True)
    jp_description = models.TextField(blank=True)

class GroupMembership(models.Model):
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_start_performance = models.ForeignKey(Performance, on_delete=models.PROTECT, related_name='group_join') # if we don't know this info, there will be a dummy Show/Production/ProductionRun/Performance
    date_end = models.DateField(null=True)
    date_end_performance = models.ForeignKey(Performance, on_delete=models.PROTECT, null=True, related_name='group_depart')
    associated_group = models.ForeignKey(GroupEnum, on_delete=models.PROTECT)
    gender_role = models.CharField( max_length=15, choices=[('otokoyaku', 'otokoyaku'), ('musumeyaku', 'musumeyaku'), ('both', 'both'), ('not_applicable', 'not_applicable'),], default='not_applicable' )

""" TODO: 
 - Photos -- headshots for staff members and chirashi/header for exhibitions. Look into library options. Easy Thumbnails? 
 - Glossary? Might be a separate app; pain in the ass to localize. Situation normal.
 - OH YEAH LOCALIZATION associated translation tables by domain; locale-slug-associated field (enums should be useful for this)-text?
"""