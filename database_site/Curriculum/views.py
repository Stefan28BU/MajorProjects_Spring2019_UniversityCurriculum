from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

from .forms import *


def index(request):
    return render(request=request, template_name="index.html")


def newCurriculum(request):

    if request.method == 'POST':
        form = newCurriculumForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = newCurriculumForm()

    return render(request=request, template_name="curriculum/newCurriculum.html", context={"form": form})


def newHead(request):
    if request.method == 'POST':
        form = headForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = headForm()

    return render(request=request, template_name="curriculum/departmentHead.html", context={"form": form})


def newCourse(request):
    return render(request=request, template_name="curriculum/newCourse.html")


def newTopic(request):
    return render(request=request, template_name="curriculum/newTopic.html")


def dashboard(request):
    curricula = Curriculum.objects.order_by('-Cur_name')[:5]
    output = ', '.join([c.Cur_name for c in curricula])
    return HttpResponse(output)
