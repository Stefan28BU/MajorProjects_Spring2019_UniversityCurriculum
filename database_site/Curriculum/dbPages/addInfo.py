from database_site.Curriculum.models import *


def add_person(person_name):
	p = Person(Name=person_name)
	p.save()


def add_curriculum(cur_name, head_id, min_hours):
	c = Curriculum(Cur_name=cur_name, Head_ID=head_id, MinHours=min_hours)
	c.save()
