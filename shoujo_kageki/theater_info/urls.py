from django.urls import path

from . import views

urlpatterns = [
    path('staff/<str:surname_romaji>_<str:given_name_romaji>_<str:suffix>.html', views.IndexView.as_view(), name='profile_wsuffix'),
    path('staff/<str:surname_romaji>_<str:given_name_romaji>.html', views.StaffProfileView.as_view(), name='profile'),
    path('staff.html', views.StaffMemberList.as_view(), name='staff'),
    path('', views.IndexView.as_view(), name='index'),
]