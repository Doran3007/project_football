from django.urls import path
from .views import index

app_name = 'football_club'

urlpatterns = [
    path('', index, name='index'),
]