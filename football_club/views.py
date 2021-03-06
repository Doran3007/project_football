from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from django.db.models import Q # новый


# Create your views here.

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


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


class SearchResultsView(ListView):
    template_name = 'search_results.html'
    model = Stadium

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('search')

        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context.update({
            'club': Club.objects.filter( Q(name__icontains=query) | Q(country__icontains=query)).order_by('name'),
            'staff': Staff.objects.filter( Q(first_name__icontains=query) | Q(second_name__icontains=query)).order_by('second_name'),
            'stadium': Stadium.objects.filter( Q(name__icontains=query) | Q(location__icontains=query)).order_by('name'),
            'trophy': Trophy.objects.filter(name__icontains=query).order_by('name'),
        })
        return context 

