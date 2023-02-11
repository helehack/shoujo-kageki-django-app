from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from datetime import datetime
from .models import *
from enum import IntEnum
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

def is_valid_year(n):
    try:
        float(n).is_integer()
    except ValueError:
        return False
    else:
        if float(n) in range(1880, 2100): # currently very arbitrary
            return True
        
        return False
        
            

class ListAs(IntEnum):
    writer = 6
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

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except StaffMember.MultipleObjectsReturned:
            return redirect(reverse('profile_disambiguation', kwargs=self.kwargs))
    
    def get_object(self):
        if 'suffix' in self.kwargs:
            return get_object_or_404(
                StaffMember,
                stagename__is_canonical=True,
                stagename__surname_romaji=self.kwargs['surname_romaji'],
                stagename__given_name_romaji=self.kwargs['given_name_romaji'],
                stagename__suffix=self.kwargs['suffix'],
            )
        
        return get_object_or_404(
            StaffMember,
            stagename__is_canonical=True,
            stagename__surname_romaji=self.kwargs['surname_romaji'],
            stagename__given_name_romaji=self.kwargs['given_name_romaji'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stagenames"] = self.object.stagename_set.all()
        context["rolelist"] = PerformanceCastPerformer.objects.filter(production_cast_member__stage_name__in=context["stagenames"])
        context["perfstafflist"] = PerformanceCastStaff.objects.filter(production_cast_member__stage_name__in=context["stagenames"])
        context["workstafflist"] = WorkStaff.objects.filter(staff_stage_name__in=context["stagenames"])
        return context

class ProfileDisambiguationList(ListView):
    model = StageName

    def get_queryset(self):
        return super().get_queryset().filter(
            surname_romaji=self.kwargs['surname_romaji'],
            given_name_romaji=self.kwargs['given_name_romaji'],
        ).distinct().order_by('suffix')

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
            ListAs.director,ListAs.conductor,ListAs.composer,ListAs.choreographer,ListAs.writer
        ]).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            qs = qs.filter(
                Q(groupmembership__date_end=None)
                |Q(groupmembership__date_end__gte=datetime.today()),
                groupmembership__associated_group=Group.staff
            )

        elif is_valid_year(self.kwargs['when']):
            qs = qs.filter(
                Q(groupmembership__date_start__year__lte=self.kwargs['when'])
                &Q(groupmembership__date_end__year__gte=self.kwargs['when']),
                groupmembership__associated_group=Group.staff
            )

        return qs

class SpecificStaffList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(list_as=ListAs[self.kwargs['staff_type']]).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            qs = qs.filter(
                Q(groupmembership__date_end=None)
                |Q(groupmembership__date_end__gte=datetime.today()),
                groupmembership__associated_group=Group.staff
            )

        elif is_valid_year(self.kwargs['when']):
            qs = qs.filter(
                Q(groupmembership__date_start__year__lte=self.kwargs['when'])
                &Q(groupmembership__date_end__year__gte=self.kwargs['when']),
                groupmembership__associated_group=Group.staff
            )

        return qs

class EveryGroupList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(list_as=ListAs.performer).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            qs = qs.filter(
                Q(groupmembership__date_end=None)
                |Q(groupmembership__date_end__gte=datetime.today()),
                groupmembership__associated_group__in=[
                    Group.hana, Group.tsuki, Group.yuki, Group.hoshi, Group.sora, Group.senka, Group.ken1
                ]
            )

        elif is_valid_year(self.kwargs['when']):
            qs = qs.filter(
                Q(groupmembership__date_start__year__lte=self.kwargs['when'])
                &Q(groupmembership__date_end__year__gte=self.kwargs['when']),
                groupmembership__associated_group__in=[
                    Group.hana, Group.tsuki, Group.yuki, Group.hoshi, Group.sora, Group.senka, Group.ken1
                ]
            )

        return qs

class SpecificGroupList(StageNameList):
    def get_queryset(self):
        qs = super().get_queryset().filter(
            list_as=ListAs.performer, groupmembership__associated_group=Group[self.kwargs['troupe']]
        ).distinct().order_by('surname_romaji')

        if self.kwargs['when']=='current':
            qs = qs.filter(
                Q(groupmembership__date_end=None)
                |Q(groupmembership__date_end__gte=datetime.today()),
                groupmembership__associated_group=Group[self.kwargs['troupe']] 
            )

        elif is_valid_year(self.kwargs['when']):
            qs = qs.filter(
                Q(groupmembership__date_start__year__lte=self.kwargs['when'])
                &Q(groupmembership__date_end__year__gte=self.kwargs['when']),
                groupmembership__associated_group=Group[self.kwargs['troupe']] 
            )

        return qs