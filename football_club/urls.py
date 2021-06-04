from django.urls import path
from .views import index, club_detail

app_name = 'football_club'

urlpatterns = [
    path('', index, name='index'),
    path('club_detail/<slug:club_slug>/', club_detail.as_view(), name='club_detail'),

    # path('Club_detail/<int:pk>/', Club_detail, name='Club_detail'),
    # path('Club_detail/', Club_detail, name='Club_detail'),
]