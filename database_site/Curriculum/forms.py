from django import forms

from .models import *

from django import forms


class headForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

        labels = {
            'Name': 'Your Name'
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class newCurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum

        fields = ['Head', 'Cur_name', 'Min_Hours']

        labels = {
            'Cur_name': 'Curriculum Name',
            'Min_Hours': 'Minimum Hours',
            'Head': 'Curriculum Head'
        }

        widgets = {
            'Cur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Min_Hours': forms.TextInput(attrs={'class': 'form-control'}),
        }

class editPersonForm(forms.Form):
    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    curr = forms.ChoiceField(choices=pChoices, label="Select a Department Head")

    name = forms.CharField(max_length=255)


class editCurriculumFrom(forms.Form):
    cTupleArray = []
    for c in Curriculum.objects.all():
        cTupleArray.append((c.Cur_name, 'Curriculum: ' + c.Cur_name + ', Head: ' + c.Head.Name + '(' + str(
            c.Head.ID) + '), Minimum Hours: ' + str(c.Min_Hours) + ', Topic Category: ' + c.Topic_Category))
    cChoices = tuple(cTupleArray)

    curr = forms.ChoiceField(choices=cChoices, label="Select a Curriculum")

    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    newHead = forms.ChoiceField(choices=pChoices, label="Select a New Head")

    newHours = forms.IntegerField(initial=0, label="Enter New Credit Hours")


class newGoalForm(forms.ModelForm):

    class Meta:

        model = Goal

        fields = ['Associated_Curriculum', 'Description']

        labels = {
            'Associated_Curriculum': 'Curriculum',
            'Description': 'Description'
        }

        widgets = {
            'Description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class newCourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = ['Subject_Code', 'Course_Number', 'Course_Name', 'Credit_Hours', 'Description']

        labels = {
            'Subject_Code': 'Subject Code',
            'Course_Number': 'Course Number',
            'Course_Name': 'Course Name',
            'Credit_Hours': 'Credit_Hours',
            'Description': 'Description'
        }

        widgets = {
            'Subject_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'Course_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Course_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Credit_Hours': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class newTopicForm(forms.ModelForm):

    class Meta:

        model = Topic

        fields = ['Name']

        labels = {
            'Name': 'Topic Name'
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class gradeDistForm(forms.Form):
    AP = 'A+'
    A = 'A'
    AM = 'A-'
    BP = 'B+'
    B = 'B'
    BM = 'B-'
    CP = 'C+'
    C = 'C'
    CM = 'C-'
    DP = 'D+'
    D = 'D'
    DM = 'D-'
    F = 'F'
    W = 'W'
    I = 'I'

    grades = (
        (AP, 'A+'),
        (A, 'A'),
        (AM, 'A-'),
        (BP, 'B+'),
        (B, 'B'),
        (BM, 'B-'),
        (CP, 'C+'),
        (C, 'C'),
        (CM, 'C-'),
        (DP, 'D+'),
        (D, 'D'),
        (DM, 'D-'),
        (F, 'Fail'),
        (W, 'Withdraw'),
        (I, 'Incomplete')
    )

    letterGrade = forms.ChoiceField(choices=grades, label="Select a Grade")

    dist = forms.IntegerField(initial=0, label="Enter Number of Students")

    secTupleArray = []
    for s in CourseSection.objects.all():
        spring = 'SP'
        summer = 'SM'
        fall = 'FA'
        winter = 'WI'
        sem = ''

        if s.semesters == spring:
            sem = 'Spring'

        if s.semesters == summer:
            sem = 'Summer'

        if s.semesters == fall:
            sem = 'Fall'

        if s.semesters == winter:
            sem = 'Winter'

        secTupleArray.append((s.Section_ID, 'Course: ' + s.Associated_Course.Course_Name + ', Section: ' + sem + ' ' + str(s.Year)))

    secChoice = tuple(secTupleArray)

    section = forms.ChoiceField(choices=secChoice, label="Choose a Section")

    TupleArray = []
    for g in Goal.objects.all():
        TupleArray.append((g.ID, 'Goal: ' + g.Description))

    gChoice = tuple(TupleArray)
    print(gChoice)
    goal = forms.ChoiceField(choices=gChoice, label="Choose a Goal")


class newSectionForm(forms.Form):
    TupleArray = []
    for g in Course.objects.all():
        TupleArray.append((g.pk, 'Course: ' + g.Subject_Code + g.Course_Number + ' (' + g.Course_Name + ')'))

    gChoice = tuple(TupleArray)

    cName = forms.ChoiceField(choices=gChoice, label="Choose a Course")
    year = forms.IntegerField(initial=0, label="Enter a Year")

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring semester'),
        (summer, 'Summer semester'),
        (fall, 'Fall semester'),
        (winter, 'Winter semester')
    )

    seme = forms.ChoiceField(choices=semesters, label="Choose a Semester")
    enroll = forms.CharField(max_length=255, label="Enter Enrollment")

    com1 = forms.CharField(max_length=255, label="Enter First Comment")
    com2 = forms.CharField(max_length=255, label="Enter Second Comment")

