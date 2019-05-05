from database_site.Curriculum.models import *
from django.db.utils import IntegrityError

def add_person(person_name):
	p = Person(Name=person_name)
	try:
		p.save()
		return p, True
	except IntegrityError:
		return p, False


def add_curriculum(cur_name, head, min_hours):
	c = Curriculum(Cur_name=cur_name, Head=head, Min_Hours=min_hours)
	try:
		c.save()
		return c, True
	except IntegrityError:
		return c, False


def add_course(subject_code, course_number, course_name, credit_hours, description):
	c = Course(Subject_Code=subject_code, Course_Number=course_number, Course_Name=course_name,
		Description=description, Credit_Hours=credit_hours)
	try:
		c.save()
		return c, True
	except IntegrityError:
		return c, False


def add_course_curriculum(curriculum, course, required):
	cc = CurriculumCourse(Required=required, Associated_Curriculum=curriculum, Associated_Course=course)
	try:
		cc.save()
		return cc, True
	except IntegrityError:
		return cc, False


def add_topic(name):
	t = Topic(Name=name)
	try:
		t.save()
		return t, True
	except IntegrityError:
		return t, False


def add_course_topic(course, topic, units):
	ct = CourseTopics(Associated_Course=course, Associated_Topic=topic, Units=units)
	try:
		ct.save()
		return ct, True
	except IntegrityError:
		return ct, False


def add_curriculum_topic(curriculum, topic, level, subject, units):
	ct = CurriculumTopic(Associated_Curriculum=curriculum, Associated_Topic=topic, Level=level,
	                     Subject_Area=subject, Units=units)
	try:
		ct.save()
		return ct, True
	except IntegrityError:
		return ct, False


def add_grade_to_course_section(course_section, grade):
	grade = Grade(Letter_Grade=grade, Associated_Course_Section=course_section)
	try:
		grade.save()
		return grade, True
	except IntegrityError:
		return grade, False


def add_grade_to_goal(goal, grade):
	grade = Grade(Letter_Grade=grade, Assocaited_Goal=goal)
	try:
		grade.save()
		return grade, True
	except IntegrityError:
		return grade, False


def add_course_section(course, semester, year, enrollment):
	cs = CourseSection(Associated_Course=course, Year=year, Semester=semester, Enrollment=enrollment, Comment1="",
	                   Comment2="")
	try:
		cs.save()
		return cs, True
	except IntegrityError:
		return cs, False


def add_goal(curriculum, description):
	g = Goal(Associated_Curriculum=curriculum, Description=description)
	try:
		g.save()
		return g, True
	except IntegrityError:
		return g, False


def add_course_goal(course, goal):
	cg = CourseGoal(Associated_Course=course, Associated_Goal=goal)
	try:
		cg.save()
		return cg, True
	except IntegrityError:
		return cg, False
