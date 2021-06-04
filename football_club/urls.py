from django.urls import path
from .views import *

app_name = 'football_club'

urlpatterns = [
    path('', HomeShow.as_view(), name='home'),
    path('club/<slug:club_slug>/', ClubShow.as_view(), name='club'),

]