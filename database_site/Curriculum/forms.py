from django import forms

from Curriculum.models import Curriculum

class CurriculumForm:
    class Meta:
        model = Curriculum
        fields = "__all__"


