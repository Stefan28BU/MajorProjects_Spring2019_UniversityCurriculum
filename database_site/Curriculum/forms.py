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
