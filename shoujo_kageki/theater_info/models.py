from django.db import models
from django.utils.timezone import get_current_timezone, make_aware, now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Language(models.TextChoices):
    ENGLISH = 'en-US','English'
    JAPANESE = 'ja-JP','日本語'

class ProfileTextChoice(models.TextChoices):
    BLOOD_TYPE = 'blood_type', _('Blood Type')
    NICKNAME = 'nickname', _('Nickname')
    FLOWER = 'flower', _('Favorite Flower')
    FOOD = 'food', _('Favorite Food')
    COLOR = 'color', _('Favorite Color')
    HOBBY = 'hobby', _('Hobby')
    COLLECTION = 'collection', _('Collection'),
    TALENT = 'talent', _('Special Talent')
    NAME_ORIGIN = 'name_origin', _('Origin of Stage Name')
    ROLE = 'role', _('Favorite Role')
    LIKE_TO_PLAY = 'like_to_play', _('Would Like to Try Playing')
    TRIVIA = 'trivia', _('Trivia')

class LinkTypeChoice(models.TextChoices):
    INSTAGRAM = 'instagram', _('Instagram')
    TWITTER = 'twitter', _('Twitter')
    FANCLUB = 'fanclub', _('Official Fanclub')
    BLOG = 'blog', _('Blog')
    WEBSITE = 'website', _('Personal Website')
    OTHER = 'other', _('Other')

class StageGenderRole(models.TextChoices):
    OTOKOYAKU = 'otokoyaku', _('Otokoyaku')
    MUSUMEYAKU = 'musumeyaku', _('Musumeyaku')
    BOTH = 'both', _('Both')
    UNKNOWN = 'unknown', _('Unknown')

class TroupeRole(models.TextChoices):
    MEMBER = 'member', _('Member')
    TOP_STAR = 'top_star', _('Top Star')
    TOP_MUSUMEYAKU = 'top_musumeyaku', _('Top Musumeyaku')
    NIBANTE = 'nibante', _('Nibante')
    PRETOP_STAR = 'pretop_star', _('Star (Pre-Top Star System)')
    KUMICHOU = 'kumichou', _('Kumichou')
    FUKUKUMICHOU = 'fukukumichou', _('Vice Kumichou')
    UNKNOWN = 'unknown', _('Unknown')

# custom ENUM tables essentially #
class AnyEnum(models.Model):
    enum = models.CharField(max_length=20)

    def __str__(self):
        return self.enum

    class Meta:
        abstract = True

class GroupEnum(AnyEnum):
    pass

class TriggerEnum(AnyEnum):
    pass

class GenreEnum(AnyEnum):
    pass

class VenueEnum(AnyEnum):
    pass

class SourceMaterialEnum(AnyEnum):
    pass

class StageName(models.Model):
    surname = models.CharField(max_length=255)
    surname_reading = models.CharField(max_length=255)
    surname_romaji = models.CharField(max_length=255)
    given_name = models.CharField(max_length=255)
    given_name_reading = models.CharField(max_length=255)
    given_name_romaji = models.CharField(max_length=255)
    suffix = models.CharField(max_length=10, blank=True)
    associated_staff_member = models.ForeignKey('theater_info.StaffMember', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [ models.UniqueConstraint(fields=['surname_romaji', 'given_name_romaji', 'suffix'], name='Combination of romaji reading and suffix should be unique as it will be used as a URL slug.') ]
    
    def __str__(self):
        return (self.surname + self.given_name + " " + self.surname_romaji + " " + self.given_name_romaji)

class StaffMember(models.Model):
    birthdate = models.DateField(null=True, blank=True) # TODO: Solve the bday problem. Break this out into year/mo/date fields?
    deathdate = models.DateField(null=True, blank=True)
    birth_country = models.CharField(max_length=255, blank=True, default='日本国')
    birth_prefecture = models.CharField(max_length=255, blank=True)
    birth_city = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    surname_reading = models.CharField(max_length=255, blank=True)
    surname_romaji = models.CharField(max_length=255, blank=True)
    given_name = models.CharField(max_length=255, blank=True)
    given_name_reading = models.CharField(max_length=255, blank=True)
    given_name_romaji = models.CharField(max_length=255, blank=True)
    canonical_stage_name = models.OneToOneField(StageName, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.canonical_stage_name) + " (" + self.surname + self.given_name + " " + self.surname_romaji + " " + self.given_name_romaji + ")" 

class StaffProfileTextField(models.Model):
    associated_staff_member = models.ForeignKey(StaffMember, on_delete=models.PROTECT)
    profile_text_choice = models.CharField(max_length=15, choices=ProfileTextChoice.choices)
    jp_text = models.CharField(max_length=255, blank=True)
    en_text = models.CharField(max_length=255, blank=True)
    show_on_profile = models.BooleanField(default=True)
    source_material = models.CharField(max_length=255, default='Unknown')
    source_year = models.CharField(max_length=4, default='None')

    def __str__(self):
        return str(self.profile_text_choice)

class StaffProfileLink(models.Model):
    associated_staff_member = models.ForeignKey(StaffMember, on_delete=models.PROTECT)
    link_type = models.CharField(max_length=15, choices=LinkTypeChoice.choices)
    if_link_type_is_other = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255)

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
    source_material_original_language = models.CharField(max_length=255, blank=True)
    source_material_english_translation = models.CharField(max_length=255, blank=True)
    source_author_original_language = models.CharField(max_length=255, blank=True)
    source_author_english_transliteration =  models.CharField(max_length=255, blank=True)
    source_material_type = models.ManyToManyField(SourceMaterialEnum, blank=True)

    def __str__(self):
        return self.name + " " + self.romaji

class WorkStaff(models.Model):
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    work_staff_role = models.CharField(max_length=15, choices=[
        ('writer', 'Writer'), ('choreographer', 'Choreographer'),('composer','Composer')
    ])
    staff_stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.staff_stage_name) + " (" + self.work_staff_role + ")"

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
    # some kind of way to add trivia

    def __str__(self):
        works_str = ''

        for work in self.works.all():
            works_str += str(work)
        
        return works_str

class ProductionCastMember(models.Model):
    production = models.ForeignKey(Production, on_delete=models.PROTECT)
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.stage_name)

class ProductionRun(models.Model):
    production = models.ForeignKey(Production, on_delete=models.PROTECT)
    venue = models.ForeignKey(VenueEnum, on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return str(self.venue) + " (" + str(self.date_start.year) + "/" + str(self.date_start.month) + " through " + str(self.date_end.year) + "/" + str(self.date_end.month) + ")"

class Performance(models.Model): #TODO: act 1/2 shinko casts??? 
    work = models.ForeignKey(Work, on_delete=models.PROTECT)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    tour_venue = models.CharField(max_length=255, blank=True) # for encapsulating national tour information
    associated_production_run = models.ForeignKey(ProductionRun, on_delete=models.PROTECT)
    
    def __str__(self):
        return str(self.work) + " -- " + str(self.associated_production_run)

class PerformanceCastMember(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    production_cast_member = models.ForeignKey(ProductionCastMember, on_delete=models.PROTECT)
    role = models.ForeignKey(NamedRole, on_delete=models.PROTECT)
    was_final_performance_for = models.BooleanField()
    was_first_performance_for = models.BooleanField()

    def __str__(self):
        return str(self.role)

class PerformanceStaff(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.PROTECT)
    stage_name = models.ForeignKey(StageName, on_delete=models.PROTECT)
    performance_staff_role = models.CharField(max_length=15, choices=[('director','Director'),('conductor','Conductor'),])

    def __str__(self):
        return str(self.performance_staff_role)

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
    date_start = models.DateField(null=True, blank=True)
    date_start_performance = models.ForeignKey(Performance, on_delete=models.SET_NULL, null=True, blank=True, related_name='performance_joined_group') # if we don't know this info, there will be a dummy Show/Production/ProductionRun/Performance
    date_end = models.DateField(null=True, blank=True)
    date_end_performance = models.ForeignKey(Performance, on_delete=models.SET_NULL, null=True, blank=True, related_name='group_depart')
    associated_group = models.ForeignKey(GroupEnum, on_delete=models.PROTECT)
    stage_gender_role = models.CharField(max_length=15, choices=StageGenderRole.choices, blank=True)
    troupe_role = models.CharField(max_length=15, choices=TroupeRole.choices, blank=True)

""" TODO: 
 - Photos -- headshots for staff members and chirashi/header for exhibitions. Look into library options. Easy Thumbnails? 
 - Glossary? Might be a separate app; pain in the ass to localize. Situation normal.
 - OH YEAH LOCALIZATION associated translation tables by domain; locale-slug-associated field (enums should be useful for this)-text?
"""