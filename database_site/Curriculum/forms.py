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
        pTupleArray.append((p, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    extensive = 'EX'
    inclusive = 'IN'
    basicPlus = 'BP'
    basic = 'BC'
    unsatisfactory = 'US'
    substandard = 'SB'

    topicCategories = (
        (extensive, 'Extensive'),
        (inclusive, 'Inclusive'),
        (basicPlus, 'BasicPlus'),
        (basic, 'Basic'),
        (unsatisfactory, 'Unsatisfactory'),
        (substandard, 'Substandard'),
    )

    leader = forms.ChoiceField(choices=pChoices, label='Curriculum Head')

    class Meta:
        model = Curriculum

        fields = ['Cur_name', 'Head', 'Min_Hours']

        labels = {
            'Cur_name': 'Curriculum Name',
            'Head': 'Your ID',
            'Min_Hours': 'Minimum Hours'
        }

        widgets = {
            'Cur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Head': forms.TextInput(attrs={'class': 'form-control'}),
            'Min_Hours': forms.TextInput(attrs={'class': 'form-control'}),
        }
