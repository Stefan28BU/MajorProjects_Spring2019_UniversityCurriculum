from database_site.Curriculum.models import *


def get_curricula():
	return Curriculum.objects.order_by('Cur_name')


def get_curricula_heads():
	return Person.objects.all()


def get_courses_in_curricula(cur_name):
	course_names = CurriculumCourse.objects.filter(Cur_name=cur_name).values('Course_Name')
	courses = Course.objects.filter(Course_Name__in)

