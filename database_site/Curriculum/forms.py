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
            'Head': forms.Select(attrs={'class': 'selectpicker form-control'}),

            'Cur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Min_Hours': forms.TextInput(attrs={'class': 'form-control'}),
        }


class editPersonForm(forms.Form):
    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    curr = forms.ChoiceField(choices=pChoices, label="Select a Department Head",widget= forms.Select(attrs={'class': 'selectpicker form-control'}))

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), label="New Name")


class editCurriculumFrom(forms.Form):
    cTupleArray = []
    for c in Curriculum.objects.all():
        cTupleArray.append((c.Cur_name, 'Curriculum: ' + c.Cur_name + ', Head: ' + c.Head.Name + '(' + str(
            c.Head.ID) + '), Minimum Hours: ' + str(c.Min_Hours) + ', Topic Category: ' + c.Topic_Category))
    cChoices = tuple(cTupleArray)

    curr = forms.ChoiceField(choices=cChoices, label="Select a Curriculum",widget= forms.Select(attrs={'class': 'selectpicker form-control'}))

    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    newHead = forms.ChoiceField(choices=pChoices, label="Select a New Head", widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    newHours = forms.IntegerField(initial=0, label="Enter New Credit Hours", widget= forms.TextInput(attrs={'class': 'form-control'}))


class newGoalForm(forms.ModelForm):

    class Meta:

        model = Goal

        fields = ['Associated_Curriculum', 'Description']

        labels = {
            'Associated_Curriculum': 'Curriculum',
            'Description': 'Description'
        }

        widgets = {
            'Associated_Curriculum':  forms.Select(attrs={'class': 'selectpicker form-control'}),

            'Description':  forms.TextInput(attrs={'class': 'form-control'}),
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

    letterGrade = forms.ChoiceField(choices=grades, label="Select a Grade", widget= forms.Select(attrs={'class': 'selectpicker form-control'}))

    dist = forms.IntegerField(initial=0, label="Enter Number of Students", widget=forms.TextInput(attrs={'class': 'form-control'}))

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

    section = forms.ChoiceField(choices=secChoice, label="Choose a Section",widget= forms.Select(attrs={'class': 'selectpicker form-control'}))

    TupleArray = []
    for g in Goal.objects.all():
        TupleArray.append((g.ID, 'Goal: ' + g.Description))

    gChoice = tuple(TupleArray)
    print(gChoice)
    goal = forms.ChoiceField(choices=gChoice, label="Choose a Goal",widget= forms.Select(attrs={'class': 'selectpicker form-control'}))


class newSectionForm(forms.Form):
    TupleArray = []
    for g in Course.objects.all():
        TupleArray.append((g.pk, 'Course: ' + g.Subject_Code + g.Course_Number + ' (' + g.Course_Name + ')'))

    gChoice = tuple(TupleArray)

    cName = forms.ChoiceField(choices=gChoice, label="Choose a Course",widget= forms.Select(attrs={'class': 'selectpicker form-control'}))
    year = forms.IntegerField(initial=0, label="Enter a Year", widget= forms.TextInput(attrs={'class': 'form-control'}))

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring'),
        (summer, 'Summer'),
        (fall, 'Fall'),
        (winter, 'Winter')
    )

    seme = forms.ChoiceField(choices=semesters, label="Choose a Semester", widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    enroll = forms.CharField(max_length=255, label="Enter Enrollment", widget=forms.TextInput(attrs={'class': 'form-control'}))

    com1 = forms.CharField(max_length=255, label="Enter First Comment",widget=forms.TextInput(attrs={'class': 'form-control'}))
    com2 = forms.CharField(max_length=255, label="Enter Second Comment",widget=forms.TextInput(attrs={'class': 'form-control'}))


class editCourseForm(forms.Form):
    eCTupleArray = []
    for g in Course.objects.all():
        eCTupleArray.append((g.pk, 'Course: ' + g.Subject_Code + g.Course_Number + ' (' + g.Course_Name + ')'))

    ecChoice = tuple(eCTupleArray)

    course = forms.ChoiceField(choices=ecChoice, label="Choose a Course",widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    newName = forms.CharField(max_length=255, label="Enter New Name",widget=forms.TextInput(attrs={'class': 'form-control'}))
    newCode = forms.CharField(max_length=255, label="Enter New Subject Code",widget=forms.TextInput(attrs={'class': 'form-control'}))
    newNum = forms.CharField(max_length=255, label="Enter New Course Number",widget=forms.TextInput(attrs={'class': 'form-control'}))
    newCred = forms.IntegerField(initial=0, label="Enter New Hours",widget=forms.TextInput(attrs={'class': 'form-control'}))
    newDes = forms.CharField(max_length=255, label="Enter New Description",widget=forms.TextInput(attrs={'class': 'form-control'}))

    tpTupleArray = []
    for g in Topic.objects.all():
        tpTupleArray.append((g.ID, g.Name))

    tpChoice = tuple(tpTupleArray)

    topic = forms.ChoiceField(choices=tpChoice, label="Choose a Topic", widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

