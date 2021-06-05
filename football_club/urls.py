from django.urls import path
from .views import *

app_name = 'football_club'

urlpatterns = [
    path('', HomeShow.as_view(), name='home'),
    path('club/<slug:club_slug>/', ClubShow.as_view(), name='club'),
    path('stadium/<slug:stadium_slug>/', StadiumShow.as_view(), name='stadium'),
    path('staff/<slug:staff_slug>/', StaffShow.as_view(), name='staff'),
    path('staff/', StaffListShow.as_view(), name='staff_list'),
    path('trophy/<slug:trophy_slug>/', TrophyShow.as_view(), name='trophy'),
]