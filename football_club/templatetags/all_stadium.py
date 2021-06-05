from django import template
from football_club.models import *

register = template.Library()

@register.inclusion_tag('club/stadium_list.html')    #register function in template
def stadium_list():
    stadium = Stadium.objects.all        #take 5 last comments
    return {'stadium': stadium}

@register.inclusion_tag('club/trophy_list.html')    #register function in template
def trophy_list():
    trophy = Trophy.objects.all        #take 5 last comments
    return {'trophy': trophy}