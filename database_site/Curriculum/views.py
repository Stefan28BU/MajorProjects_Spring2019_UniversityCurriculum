from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

from .forms import *
from pprint import pprint

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
    if request.method == 'POST':
        form = newCourseForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = newCourseForm()

    return render(request=request, template_name="curriculum/newCourse.html", context={"form": form})


def newTopic(request):
    if request.method == 'POST':
        form = newTopicForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = newTopicForm()

    return render(request=request, template_name="curriculum/newTopic.html", context={"form": form})


def newGoal(request):
    if request.method == 'POST':
        form = newGoalForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = newGoalForm()

    return render(request=request, template_name="curriculum/newGoal.html", context={"form": form})

def dashboard(request):
    curricula = Curriculum.objects.order_by('-Cur_name')[:5]
    output = ', '.join([c.Cur_name for c in curricula])
    return HttpResponse(output)


def editPerson(request):
    if request.method == 'POST':
        form = editPersonForm(request.POST)

        if form.is_valid():
            temp = Person.objects.get(ID=form['curr'].value())

            temp.Name = form['name'].value()
            temp.save()

            print("person ", temp.Name)

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = editPersonForm()

    return render(request=request, template_name="Edit/editPerson.html", context={"form": form})

def pickCuricToEdit(request):
    if request.method == 'POST':
        form = pickCuricToEditForm(request.POST)

        return HttpResponseRedirect('/Curriculum/editSpecificCurriculum/' + str(form['curr'].value()))
    else:
        form = pickCuricToEditForm()

    return render(request=request, template_name="Edit/pickCurriculumToEdit.html", context={"form": form})


def editCurriculum(request, curr_id):
    pprint(vars(request))
    if request.method == 'POST':
        form = editCurriculumForm(request.POST)

        if form.is_valid():
            temp = Curriculum.objects.get(Cur_name=form['curr'].value())
            tempPerson = Person.objects.get(ID=form['newHead'].value())

            temp.Head = tempPerson
            temp.Min_Hours = form['newHours'].value()

            temp.save()


        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = editCurriculumForm()

    return render(request=request, template_name="Edit/editCurriculum.html", context={"form": form})


def gradeDist(request):
    if request.method == 'POST':
        form = gradeDistForm(request.POST)

        if form.is_valid():
            temp = Grade()

            temp.dist_number = form['dist'].value()
            temp.Letter_Grade = form['letterGrade'].value()
            temp.Associated_Goal = Goal.objects.get(ID=form['goal'].value())
            temp.Associated_Course_Section = CourseSection.objects.get(Section_ID=form['section'].value())

            temp.save()


        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = gradeDistForm()

    return render(request=request, template_name="curriculum/gradeDist.html", context={"form": form})


def newSection(request):
    if request.method == 'POST':
        form = newSectionForm(request.POST)

        if form.is_valid():
            temp = CourseSection()

            temp.Semester = form['seme'].value()
            temp.Year = form['year'].value()
            temp.Comment1 = form['com1'].value()
            temp.Comment2 = form['com2'].value()
            temp.Enrollment = form['enroll'].value()
            temp.Associated_Course = Course.objects.get(pk=form['cName'].value())

            temp.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = newSectionForm()

    return render(request=request, template_name="curriculum/newSection.html", context={"form": form})


def editCourse(request):
    if request.method == 'POST':
        form = editCourseForm(request.POST)

        if form.is_valid():
            temp = Course.objects.get(pk=form['course'].value())
            temp.Course_Number = form['newNum'].value()
            temp.Credit_Hours = form['newCred'].value()
            temp.Description = form['newDes'].value()
            temp.Course_Name = form['newName'].value()
            temp.Subject_Code = form['newCode'].value()
            temp.save()

            tempTopic = Topic.objects.get(ID=form['topic'].value())

            tempCourseTopic = CourseTopics()
            tempCourseTopic.Associated_Course = temp
            tempCourseTopic.Associated_Topic = tempTopic

            try:
                tempCourseTopic.save()
            except:
                print("Already Exists")

            tempGoal = Goal.objects.get(ID=form['goal'].value())
            tempCourseGoal  = CourseGoal()
            tempCourseGoal.Associated_Course = temp
            tempCourseGoal.Associated_Goal = tempGoal
            try:
                tempCourseGoal.save()
            except:
                print("Already Exists")
        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = editCourseForm()

    return render(request=request, template_name="Edit/editCourse.html", context={"form": form})


def editTopic(request):
    if request.method == 'POST':
        form = editTopicForm(request.POST)

        if form.is_valid():
            temp = Topic.objects.get(ID=form['topic'].value())
            temp.Name = form['name'].value()

            temp.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = editTopicForm()

    return render(request=request, template_name="Edit/editTopic.html", context={"form": form})


def editGoal(request):
    if request.method == 'POST':
        form = editGoalForm(request.POST)

        if form.is_valid():
            tempGoal = Goal.objects.get(ID=form['goal'].value())
            tempGoal.Description = form['des'].value()

            tempCurr = Curriculum.objects.get(Cur_name=form['curr'].value())
            tempGoal.Associated_Curriculum = tempCurr
            tempGoal.save()

        else:
            print('Invalid')
            return HttpResponseRedirect('/Curriculum')
    else:
        form = editGoalForm()

    return render(request=request, template_name="Edit/editGoal.html", context={"form": form})

