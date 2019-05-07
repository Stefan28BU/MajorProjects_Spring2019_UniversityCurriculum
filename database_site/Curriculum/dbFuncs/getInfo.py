from Curriculum.models import *


spring = 1
summer = 2
fall = 3
winter = 4

semDict = {
	'SP': 1,
	'SM': 2,
	'FA': 3,
	'WI': 4,
}

def get_curricula():
	return Curriculum.objects.order_by('Cur_name')


def get_curricula_heads():
	return Person.objects.all()


def get_courses_in_curricula(cur_name):

	cc =  CurriculumCourse.objects.filter(Associated_Curriculum__Cur_name=cur_name)
	cName = set()
	for c in cc:
		cName.add(str(c.Associated_Course.Course_Name))
	return cName


def get_topics_in_curricula(cur_name):
	cc = CurriculumTopic.objects.filter(Associated_Curriculum__Cur_name=cur_name)
	cName = set()
	for c in cc:
		cName.add(str(c.Associated_Topic.Name))
	return cName


def get_info_on_curriculum(cur_name):
	return get_courses_in_curricula(cur_name), get_topics_in_curricula(cur_name)


def get_basic_info_on_course(subject_code, course_number):
	res = Course.objects.filter(Subject_Code=subject_code, Course_Number=course_number)
	return res.values('Course_Name', 'Credit_Hours', 'Description')


def get_basic_info_on_course_with_name(course_name):
	res = Course.objects.filter(Course_Name=course_name)
	return res


def get_curricula_info_on_course_with_name(course_name):
	return CurriculumCourse.objects.filter(Associated_Course__Course_Name=course_name)


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
	return CourseSection.objects.filter(Associated_Course__Course_Name=course_name)


def get_sections_grades_of_a_course(course_name):
	course_sections = get_all_sections(course_name)
	res = []
	print(len(course_sections), "length")
	for i in course_sections:
		print(i.Associated_Course.Course_Name + 'IIIIIIIII')
		list.append(res, Grade.objects.filter(Associated_Course_Section__Section_ID=i.Section_ID))

	return res


def get_cur_from_course_name_and_cur(course_name, cur_name):
	return CurriculumCourse.objects.filter(Associated_Curriculum__Cur_name=cur_name, Associated_Course__Course_Name=course_name)


def get_info_on_course_no_range(course_name, cur_name):

	course_sections = get_all_sections(course_name)
	print('Get all sections result: ', course_sections)
	cur = get_cur_from_course_name_and_cur(course_name, cur_name)

	res = []
	for i in course_sections:
		for j in cur:
			if j.Associated_Course.Course_Name == i.Associated_Course.Course_Name:
				res.append(i)
	res2 = []

	for i in res:
		print('Grade loop')
		grade = Grade.objects.filter(Associated_Course_Section=i)
		# grade = get_sections_grades_of_a_course(i.Associated_Course)
		res2.append(grade)
		print(grade)

	gradeDict = {
		'A+': 0,
		'A': 0,
		'A-': 0,
		'B+': 0,
		'B': 0,
		'B-': 0,
		'C+': 0,
		'C': 0,
		'C-': 0,
		'D+': 0,
		'D': 0,
		'D-': 0,
		'F': 0,
		'I': 0,
		'W': 0,
	}

	for gList in res2:
		for g in gList:
			gradeDict[g.Letter_Grade] += g.dist_number
	# Res2 is List of grades by course section
	return res2, res


def get_all_sections_with_range(course_name, start_sem, start_year, end_sem, end_year):
	res = CourseSection.objects.filter(Year__gte=start_year, Year__lte=end_year, Associated_Course=course_name)

	res2 = []
	for i in res:
		#For every course section
		if i.Year == start_year:
			#If its the start year and after the first semester, add
			if semDict[i.Semester] >= start_sem:
				res2.append(i)
		# If its the last year and before the end semester, add
		elif i.Year == end_year:
			if end_sem >= semDict[i.Semester]:
				res2.append(i)
		# If its between the years, add
		elif i.Year > start_year and i.Year < end_year:
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

	return res2, res


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














