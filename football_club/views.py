from django.shortcuts import render
from .models import Club,Trophy,Stadium,Staff

# Create your views here.
# {'clubs': football_club} here we rename data from Club model in "clubs"
def index(request):
    football_club=Club.objects.all() # Here we pull data of Club model
    return render(request, 'main/index.html', {'clubs': football_club})
