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
	cc = CurriculumCourse.objects.filter(Associated_Curriculum__Cur_name=cur_name)
	cName = set()
	for c in cc:
		cName.add(str(c.Associated_Course.Course_Name))
	return cName


def get_courses_in_curricula2(cur_name):
	cc = CurriculumCourse.objects.filter(Associated_Curriculum__Cur_name=cur_name)
	cName = set()
	for c in cc:
		cName.add(c.Associated_Course)
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
	return get_basic_info_on_course(subject_code, course_number), get_curricula_info_on_course(subject_code,
	                                                                                           course_number)


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
	return CurriculumCourse.objects.filter(Associated_Curriculum__Cur_name=cur_name,
	                                       Associated_Course__Course_Name=course_name)


def get_info_on_course_no_range(course_name, cur_name):
	course_sections = get_all_sections(course_name)
	print('Get all sections result: ', course_sections)
	cur = get_cur_from_course_name_and_cur(course_name, cur_name)

	res = []
	for i in course_sections:
		for j in cur:
			if j.Associated_Course.Course_Name == i.Associated_Course.Course_Name:
				res.append(i)

	overallDict = dict()

	for cs in res:
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
		for g in Grade.objects.filter(Associated_Course_Section=cs):
			gradeDict[g.Letter_Grade] += g.dist_number
		overallDict[str(cs.pk)] = gradeDict

	# to access a grade, q3obj[0][pk]['A+']
	# Res2 is List of grades by course section
	return overallDict, res


def get_all_sections_with_range(course_section_list, start_sem, start_year, end_sem, end_year):
	res2 = []
	for i in course_section_list:
		if start_year != '' and end_year != '':
			# For every course section
			if i.Year == int(start_year):
				# If its the start year and after the first semester, add
				if semDict[i.Semester] >= semDict[start_sem]:
					res2.append(i)
			# If its the last year and before the end semester, add
			elif i.Year == int(end_year):
				if semDict[end_sem] >= semDict[i.Semester]:
					res2.append(i)
			# If its between the years, add
			elif i.Year > int(start_year) and i.Year < int(end_year):
				res2.append(i)

	return res2


# Query3
def get_sections_grades_of_a_course_with_range(course_name, cur_name, start_semester, start_year, end_semester,
                                               end_year):
	giocnr, course_section_set = get_info_on_course_no_range(course_name, cur_name)
	course_sections = get_all_sections_with_range(course_section_set, start_semester, start_year, end_semester,
	                                              end_year)

	overallDict = dict()

	for cs in course_sections:
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
		for g in Grade.objects.filter(Associated_Course_Section=cs):
			gradeDict[g.Letter_Grade] += g.dist_number
		overallDict[str(cs.pk)] = gradeDict

	return overallDict, course_sections


def get_courses_in_a_cur(cur_name):
	return CurriculumCourse.objects.filter(Associated_Curriculum=cur_name).values('Associated_Course')


def get_sections_in_a_cur_with_time_range(cur_name, start_semester, start_year, end_semester, end_year):
	courses = get_courses_in_curricula2(cur_name)
	course_section_set = set()

	for i in courses:
		obj = get_info_on_course_no_range(i.Course_Name, cur_name)
		course_section_set.add(tuple(obj[1]))

	course_sections = []

	for i in course_section_set:
		course_sections.append(get_all_sections_with_range(i, start_semester, start_year, end_semester, end_year))

	overallDict = dict()

	for csList in course_sections:

		for cs in csList:
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

			for g in Grade.objects.filter(Associated_Course_Section__Section_ID=cs.Section_ID):
				gradeDict[g.Letter_Grade] += g.dist_number
			overallDict[str(cs.pk)] = gradeDict

	return overallDict, course_sections


def q5_ryland_style(curriculum):
	person = curriculum.Head.Name
	req_courses = 0
	opt_courses = 0
	all_course_currics = CurriculumCourse.objects.filter(Associated_Curriculum=curriculum)
	all_courses = set()
	for cc in all_course_currics:
		all_courses.add(cc.Associated_Course)
		if cc.Required:
			req_courses += 1
		else:
			opt_courses += 1

	curric_topics = CurriculumTopic.objects.filter(Associated_Curriculum=curriculum)
	curric_ct = CurriculumCT.objects.filter(Associated_Curriculum=curriculum)

	# List of curriculum topics, list of cct's associated with course topic
	topic_cct_list = set()
	for ct in curric_topics:
		list_of_cct = set()
		for c_ct in curric_ct:
			if c_ct.Associated_CT.Associated_Topic == ct.Associated_Topic:
				list_of_cct.add(c_ct)
		topic_cct_list.add((ct, tuple(list_of_cct)))



	coverage = [True, True, True, True, True, True]
	# 0 - 1 not covered
	# 1 - 2 not completely covered by required
	# 2 - 2 required don't meet min
	# 3 - 2 optionals don't complete
	# 4 - 3 not covered by min

	#   Substandard         !0
	#   Unsatisfactory      !2
	#   Basic               !3
	#   Basic+              !1
	#   Inclusive           !4
	#   Exclusive



	completed_topics = set()
	incomplete_topics = set()
	for tcct in topic_cct_list:
		u = 0
		ch = 0
		req_u = 0
		for cct in tcct[1]:
			cur_course = CurriculumCourse.objects.get(Associated_Course=cct.Associated_CT.Associated_Course,
			                                             Associated_Curriculum=curriculum)
			if cur_course.Required:
				req_u += cct.Units
			u += cct.Units
			ch += cct.Associated_CT.Associated_Course.Credit_Hours

		if req_u >= int(tcct[0].Units):
			completed_topics.add((tcct[0], str(ch)))
		else:
			incomplete_topics.add(tcct[0])
			if str(tcct[0].Level) == '1':
				coverage[0] = False
			elif str(tcct[0].Level) == '2':
				coverage[1] = False
				if req_u < float(tcct[0].Units) * curriculum.Percent_Level_2 / 100.0:
					coverage[2] = False
				elif u < tcct[0].Untis:
					coverage[3] = False
			elif str(tcct[0].Level) == '3':
				if u < float(tcct[0].Untis) * curriculum.Percent_Level_3 / 100.0:
					coverage[4] = False


	if not coverage[0]:
		top_cat = 'Substandard'
	elif not coverage[2]:
		top_cat = 'Unsatisfactory'
	elif not coverage[3]:
		top_cat = 'Basic'
	elif not coverage[1]:
		top_cat = 'Basic+'
	elif not coverage[4]:
		top_cat = 'Inclusive'
	else:
		top_cat = 'Exclusive'


	valid_goal = set()
	invalid_goal = set()
	goal_valid = True
	for g in Goal.objects.filter(Associated_Curriculum=curriculum):
		u = 0
		for cg in CourseGoal.objects.filter(Associated_Goal=g):
			u += cg.Units_Covered
		if u >= int(g.Units_For_Completion):
			valid_goal.add(g)
		else:
			goal_valid = False
			invalid_goal.add(g)


	# Person is a Person object
	# req_courses and opt_courses are required and optional
	# completed_topics is a tuple of (<curriculumTopic>, <creditHoursSpentOnIt>)
	# incomplete_topics is a list of topics not fully covered by required courses
	# valid_goal is a list of goals sufficiently covered
	# invalid goals is, well, the opposite
	# top_cat is the topic category, a string
	# goal_valid is a bool of whether it is goal valid
	# 6 Returns
	return person, (req_courses, opt_courses), (completed_topics, incomplete_topics), (valid_goal, invalid_goal), top_cat, goal_valid


def get_sections_in_a_cur_with_time_range_and_course_range(cur_name, start_semester, start_year, end_semester, end_year,
                                                           binCourse, endCourse):
	courses = get_courses_in_curricula2(cur_name)
	course_section_set = set()

	for i in courses:
		if (int(i.Course_Number) >= int(binCourse)) and (
				int(i.Course_Number) <= int(endCourse)):
			obj = get_info_on_course_no_range(i.Course_Name, cur_name)
			course_section_set.add(tuple(obj[1]))

	course_sections = []
	overallDict = dict()

	for i in course_section_set:
		course_sections.append(get_all_sections_with_range(i, start_semester, start_year, end_semester, end_year))

		for csList in course_sections:

			for cs in csList:
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

				for g in Grade.objects.filter(Associated_Course_Section__Section_ID=cs.Section_ID):
					gradeDict[g.Letter_Grade] += g.dist_number
				overallDict[str(cs.pk)] = gradeDict

	return overallDict, course_sections
