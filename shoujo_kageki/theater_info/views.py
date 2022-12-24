from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView
from .models import *

class IndexView(TemplateView):
    template_name = "index.html"

class StaffProfileView(TemplateView):
    template_name = "theater_info/staffprofile.html"

class StaffMemberList(ListView):
    model = StaffMember