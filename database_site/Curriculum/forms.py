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
    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

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
