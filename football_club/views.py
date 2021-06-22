from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


# Create your views here.

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# {'clubs': football_club} here we rename data from Club model in "clubs"
# def index(request):
#     football_club=Club.objects.all() # Here we pull data of Club model
#     return render(request, 'main/index.html', {'clubs': football_club})

class HomeShow(ListView):
    model = Club
    template_name = 'club/index.html'
    context_object_name = 'clubs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'stadium': Stadium.objects.order_by('name'),
        })
        return context

    def get_queryset(self):
        return Club.objects.order_by('name')

    # -------------Another way to compilate two model for one template---------------
    # def get_queryset(self):
    #     return Club.objects.order_by('name')

    # def get_context_data(self, **kwargs):
    #     context = super(HomeShow, self).get_context_data(**kwargs)
    #     context['stadium'] = Stadium.objects.order_by('name')
    #     return context


class ClubShow(DetailView):
    model = Club
    template_name = 'club/club.html'
    slug_url_kwarg = 'club_slug'
    context_object_name = 'club'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'stadium': Stadium.objects.order_by('name'),
        })
        context['title'] = context['club']

        return context


    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = context['club']
    #     return context

class StadiumListShow(ListView):
    model = Stadium
    template_name = 'club/_navbar.html'
    context_object_name = 'stadium'

class StadiumShow(DetailView):
    model = Stadium
    template_name = 'club/stadium.html'
    slug_url_kwarg = 'stadium_slug'
    context_object_name = 'stadium'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['stadium']
        return context

class StaffListShow(ListView):
    model = Staff
    template_name = 'club/staff_list.html'
    slug_url_kwarg = 'staff_slug'
    context_object_name = 'staff'


class StaffShow(DetailView):
    model = Staff
    template_name = 'club/staff.html'
    slug_url_kwarg = 'staff_slug'
    context_object_name = 'staff'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['staff']
        return context
    
class TrophyListShow(ListView):
    model = Trophy
    template_name = 'club/_navbar.html'
    context_object_name = 'trophy'

class TrophyShow(DetailView):
    model = Trophy
    template_name = 'club/trophy.html'
    slug_url_kwarg = 'trophy_slug'
    context_object_name = 'trophy'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['trophy']
        return context