from django.conf import settings
from django.urls import include, path

from . import views

urlpatterns = [
    path('profile/<str:surname_romaji>_<str:given_name_romaji>_<str:suffix>', views.ProfileView.as_view(), name='profile_wsuffix'),
    path('profile/<str:surname_romaji>_<str:given_name_romaji>', views.ProfileView.as_view(), name='profile'),
    path('disambig/<str:surname_romaji>_<str:given_name_romaji>', views.ProfileDisambiguationList.as_view(), name='profile_disambiguation'),
    path('performer/<str:troupe>/<str:when>', views.SpecificGroupList.as_view(), name='performer_spec'),
    path('performer/<str:when>', views.EveryGroupList.as_view(), name='performer_every'),
    path('performer', views.PerformerIndexView.as_view(), name='performer'),
#    path('performancerun/<num:id>'),
#    path('performance/<str:troupe>/<str:when>'),
#    path('performance/<str:when>'),
    path('staff/<str:staff_type>/<str:when>', views.SpecificStaffList.as_view(), name='staff_spec'),
    path('staff/<str:when>', views.EveryStaffList.as_view(), name='staff_every'),
    path('staff', views.StaffIndexView.as_view(), name='staff'),
    path('', views.IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    # NOTE: When DEBUG and staticfiles is installed, Django automatically adds static
    # urls, but does not automatically serve MEDIA
    from django.conf.urls.static import static

    # Serve static and media files from development server
    # urlpatterns += staticfiles_urlpatterns()  # automatic when DEBUG on
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    try:
        import debug_toolbar

        # Article pattern was matching and blocking these when appended, hence insert
        urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
    except ImportError:
        pass