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


