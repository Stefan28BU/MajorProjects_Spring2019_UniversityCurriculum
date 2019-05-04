from database_site.Curriculum.models import *
from django.db.utils import IntegrityError

def add_person(person_name):
	p = Person(Name=person_name)
	try:
		p.save()
		return True
	except IntegrityError:
		return False


def add_curriculum(cur_name, head, min_hours):
	c = Curriculum(Cur_name=cur_name, Head=head, Min_Hours=min_hours)
	try:
		c.save()
		return True
	except IntegrityError:
		return False


def add_course(subject_code, course_number, course_name, credit_hours, description):
	c = Course(Subject_Code=subject_code, Course_Number=course_number, Course_Name=course_name,
		Description=description, Credit_Hours=credit_hours)
	try:
		c.save()
		return True
	except IntegrityError:
		return False


def add_course_curriculum(curriculum, course, required):
	cc = CurriculumCourse(Required=required, Associated_Curriculum=curriculum, Associated_Course=course)
	try:
		cc.save()
		return True
	except IntegrityError:
		return False


def add_topic(name):
	t = Topic(Name=name)
	try:
		t.save()
		return True
	except IntegrityError:
		return False


def add_course_topic(course, topic, units):
	ct = CourseTopics(Associated_Course=course, Associated_Topic=topic, Units=units)
	try:
		ct.save()
		return True
	except IntegrityError:
		return False


def add_curriculum_topic(curriculum, topic, level, subject, units):
	ct = CurriculumTopic(Associated_Curriculum=curriculum, Associated_Topic=topic, Level=level,
	                     Subject_Area=subject, Units=units)
	try:
		ct.save()
		return True
	except IntegrityError:
		return False


def add_grade_to_course_section(course_section, grade):
	grade = Grade(Letter_Grade=grade, Associated_Course_Section=course_section)
	try:
		grade.save()
		return True
	except IntegrityError:
		return False
