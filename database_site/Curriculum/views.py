from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import *


def index(request):
    return render(request=request, template_name="index.html")


def newCurriculum(request):
    return render(request=request, template_name="curriculum/newCurriculum.html")


def dashboard(request):
    curricula = Curriculum.objects.order_by('-Cur_name')[:5]
    output = ', '.join([c.Cur_name for c in curricula])
    return HttpResponse(output)
