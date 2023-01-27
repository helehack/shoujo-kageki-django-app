from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from datetime import datetime
from .models import *
from enum import IntEnum

def is_valid_year(n):
    try:
        float(n).is_integer()
    except ValueError:
        return False
    else:
        if float(n) in range(1913, 2023):
            return True
        
        return False
        
            

class ListAs(IntEnum):
    conductor = 5
    composer = 4
    choreographer = 3
    director = 2
    performer = 1

class Group(IntEnum):
    ken1 = 8
    staff = 7
    senka = 6
    sora = 5
    hoshi = 4
    yuki = 3
    tsuki = 2
    hana = 1

class IndexView(TemplateView):
    template_name = "index.html"

class ProfileView(DetailView):
    model=StaffMember
    template_name = "theater_info/profile.html"
    
    def get_object(self):
        return StaffMember.objects.get(canonical_stage_name__surname_romaji=self.kwargs['surname_romaji'])


class PerformerIndexView(TemplateView):
    template_name = "theater_info/performer_index.html"

class StaffIndexView(TemplateView):
    template_name = "theater_info/staff_index.html"

class StageNameList(ListView):
    model = StageName
    paginate_by = 15

class EveryStaffList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(list_as__in=[
            ListAs.director,ListAs.conductor,ListAs.composer,ListAs.choreographer
        ]).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            return qs.filter(groupmembership__associated_group=Group.staff, groupmembership__date_end=None)

        return qs

class SpecificStaffList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(list_as=ListAs[self.kwargs['staff_type']]).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            return qs.filter(groupmembership__associated_group=Group.staff, groupmembership__date_end=None)

        return qs

class EveryGroupList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(list_as=ListAs.performer).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            return qs.filter(groupmembership__associated_group__in=[
                Group.hana, Group.tsuki, Group.yuki, Group.hoshi, Group.sora, Group.senka, Group.ken1
            ]).filter(
                Q(groupmembership__date_end=None)|Q(groupmembership__date_end__gte=datetime.today())
            )

        return qs

class SpecificGroupList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(
            list_as=ListAs.performer, groupmembership__associated_group=Group[self.kwargs['troupe']]
        ).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            qs = qs.filter(
                Q(groupmembership__date_end=None)|Q(groupmembership__date_end__gte=datetime.today()),
                groupmembership__associated_group=Group[self.kwargs['troupe']] 
            )

        # if is_valid_year(self.kwargs['when']):
        #     qs = qs.filter(
        #         Q(groupmembership__date_end=None)|Q(groupmembership__date_end__gte=datetime.today()),
        #         groupmembership__associated_group=Group[self.kwargs['troupe']] 
        #     )

        return qs