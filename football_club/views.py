from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# Create your views here.

class HomeShow(ListView):
    model = Club
    template_name = 'club/index.html'
    context_object_name = 'clubs'

# {'clubs': football_club} here we rename data from Club model in "clubs"
# def index(request):
#     football_club=Club.objects.all() # Here we pull data of Club model
#     return render(request, 'main/index.html', {'clubs': football_club})


def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ClubShow(DetailView):
    model = Club
    template_name = 'club/club.html'
    slug_url_kwarg = 'club_slug'
    context_object_name = 'club'
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['club']
        return context

