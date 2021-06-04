from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy 
from .models import *
from django.views.generic.detail import DetailView


# Create your views here.
# {'clubs': football_club} here we rename data from Club model in "clubs"
def index(request):
    football_club=Club.objects.all() # Here we pull data of Club model
    return render(request, 'main/index.html', {'clubs': football_club})

# def Club_detail(request):
#     football_club=Club.objects.all() # Here we pull data of Club model
#     return render(request, 'club/Club_detail.html', {'football_club': football_club})

class club_detail(DetailView):
    model = Club
    template_name = 'club_detail.html'
    slug_url_kwarg = 'club_slug'
    context_object_name = 'football_club'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
