from django.urls import path
from .views import *

app_name = 'football_stat'

urlpatterns = [
    path('dashboard', dashboardview, name='dash'),
    path('team', team_stat, name='team'),
    path('selectTeam', individualTeamData, name='selectTeam'),

]