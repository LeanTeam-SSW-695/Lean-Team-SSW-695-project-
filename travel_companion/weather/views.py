from django.shortcuts import render
from .models import Users
# Create your views here.

def weather(request):
    # weather_information = {
    #     'report' : report
    # }
    return render(request, 'weather/home.html')

def about(request):
    return render(request, 'weather/about.html', {'title':'About'})