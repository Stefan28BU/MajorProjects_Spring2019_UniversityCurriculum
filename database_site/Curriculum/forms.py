from django import forms

from Curriculum.models import *

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

    tpc = forms.ChoiceField(choices=topicCategories, label='Topic Category')

    class Meta:
        model = Curriculum

        fields = ['tpc', 'Cur_name', 'Head', 'Min_Hours']

        labels = {
            'tpc': 'Topic Category',
            'Cur_name': 'Curriculum Name',
            'Head': 'Your ID',
            'Min_Hours': 'Minimum Hours'
        }

        widgets = {
            'Cur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Head': forms.TextInput(attrs={'class': 'form-control'}),
            'Min_Hours': forms.TextInput(attrs={'class': 'form-control'}),
        }
