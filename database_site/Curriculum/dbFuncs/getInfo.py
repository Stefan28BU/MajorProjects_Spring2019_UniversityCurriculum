from Curriculum.models import *


spring = 1
summer = 2
fall = 3
winter = 4


def get_curricula():
	return Curriculum.objects.order_by('Cur_name')


def get_curricula_heads():
	return Person.objects.all()


def get_courses_in_curricula(cur_name):
	return CurriculumCourse.objects.filter(Associated_Curriculum=cur_name).values('Associated_Course')


def get_topics_in_curricula(cur):
	return CurriculumTopic.objects.filter(Associated_Curriculum=cur).values('Associated_Topic')


def get_info_on_curriculum(cur_name):
	return get_courses_in_curricula(cur_name), get_topics_in_curricula(cur_name)


def get_basic_info_on_course(subject_code, course_number):
	res = Course.objects.filter(Subject_Code=subject_code, Course_Number=course_number)
	return res.values('Course_Name', 'Credit_Hours', 'Description')


def get_basic_info_on_course_with_name(course_name):
	res = Course.objects.filter(Course_Name=course_name)
	return res.values('Subject_Code', 'Course_Number', 'Credit_Hours', 'Description')


def get_curricula_info_on_course_with_name(course_name):
	return CurriculumCourse.objects.filter(Associated_Course=course_name).values('Associated_Curriculum')


def get_course_name_from_code(subject_code, course_number):
	return Course.objects.filter(Subject_Code=subject_code, Course_Number=course_number).values('Course_Name')


def get_curricula_info_on_course(subject_code, course_number):
	course_name = get_course_name_from_code(subject_code, course_number)
	return CurriculumCourse.objects.filter(Associated_Course=course_name).values('Associated_Curriculum')


def get_info_on_course(subject_code, course_number):
	return get_basic_info_on_course(subject_code, course_number), get_curricula_info_on_course(subject_code, course_number)


def get_info_on_course_with_name(course_name):
	return get_basic_info_on_course_with_name(course_name), get_curricula_info_on_course_with_name(course_name)


def get_all_sections(course_name):
	return CourseSection.objects.filter(Associated_Course=course_name)


def get_sections_grades_of_a_course(course_name):
	course_sections = get_all_sections(course_name)
	res = []
	for i in course_sections:
		list.append(res, Grade.objects.filter(Associated_Course_Section=i))

	return res


def get_cur_from_course_name_and_cur(course_name, cur_name):
	return CurriculumCourse.objects.filter(Associated_Curriculum=cur_name, Associated_Course=course_name)


def get_info_on_course_no_range(course_name, cur_name):
	course_sections = get_all_sections(course_name)
	cur = get_cur_from_course_name_and_cur(course_name, cur_name)
	res = []
	for i in course_sections:
		list.append(res, cur.objects.filter(Associated_Course=i.Associated_Course))

	res2 = []

	for i in res:
		res2 = get_sections_grades_of_a_course(i.Associated_Course)

	return res2


def get_all_sections_with_range(course_name, start_sem, start_year, end_sem, end_year):
	res = CourseSection.objects.filter(Year__gte=start_year, Year__lte=end_year, Associated_Course=course_name)

	res2 = []
	for i in res:
		if i.Year == start_year:
			if start_sem == spring:
				res2.append(i)
			else:
				if i.Semester >= start_sem:
					res2.append(i)

		elif i.Year == end_year:
			if end_year == winter:
				res2.append(i)
			else:
				if i.Semester <= end_sem:
					res2.append(i)
		else:
			res2.append(i)

	return res2


#Query3
def get_sections_grades_of_a_course_with_range(course_name, cur_name, start_semester, start_year, end_semester, end_year):
	course_sections = get_all_sections_with_range(course_name, start_semester, start_year, end_semester, end_year)
	cur = get_cur_from_course_name_and_cur(course_name, cur_name)
	res = []

	for i in course_sections:
		res.append(cur.objects.filter(Associated_Course=i.Associated_Course))

	res2 = []

	for i in res:
		res2 = get_sections_grades_of_a_course(i.Associated_Course)

	return res2


def get_courses_in_a_cur(cur_name):
	return CurriculumCourse.objects.filter(Associated_Curriculum=cur_name).values('Associated_Course')


def get_sections_in_a_cur_with_time_range(cur_name, start_semester, start_year, end_semester, end_year):
	courses_in_a_cur = get_courses_in_a_cur(cur_name)
	res = []

	for i in courses_in_a_cur:
		res.append(get_all_sections(i))

	res2 = []

	for i in res:
		if (i.Year >= start_year) and (i.Year <= end_year):
			res2.append(i)

	for i in res:
		if i.Year == start_year:
			if start_semester == spring:
				res2.append(i)
			else:
				if i.Semester >= start_semester:
					res2.append(i)
		elif i.Year == end_year:
			if end_year == winter:
				res2.append(i)
			else:
				if i.Semester <= end_semester:
					res2.append(i)
		else:
			res2.append(i)

	res3 = [] 

	for i in res2:
		res3.append(Grade.objects.filter(Associated_Course_Section=i))

	return res3














