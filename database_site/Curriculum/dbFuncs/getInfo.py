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

    topic_cct_list = set()
    for ct in curric_topics:
        list_of_cct = set()
        for c_ct in curric_ct:
            if c_ct.Associated_CT.Associated_Topic == ct.Associated_Topic:
                list_of_cct.add(c_ct)
        topic_cct_list.add((ct, tuple(list_of_cct)))

    completed_topics = set()
    for tcct in topic_cct_list:
        u = 0
        ch = 0
        for cct in tcct[1]:
            u += cct.Units
            ch += cct.Associated_CT.Associated_Course.Credit_Hours

        if u >= tcct[0].Units:
            completed_topics.add((tcct[0], str(ch)))

    curric_cg = set()
    curric_g = Goal.objects.filter(Associated_Curriculum=curriculum)
    for g in curric_g:
        g_cg = CourseGoal.objects.filter(Associated_Goal=g)
        for cg in g_cg:
            curric_cg.add(cg)

    course_cg = set()
    for c in all_courses:
        c_cg = CourseGoal.objects.filter(Associated_Course=c)
        for cg in c_cg:
            course_cg.add(cg)

    leftover_course_goals = curric_cg - course_cg
    leftover_goals = set()
    for g in leftover_course_goals:
        leftover_goals.add(g.Associated_Goal)

    # Person is a Person object
    # req_courses and opt_courses are required and optional
    # completed_topics is a tuple of (<curriculumTopic>, <creditHoursSpentOnIt>)
    # leftover goals is a set of Goal objects that are not completed
    # If it is empty, then it is goal valid, otherwise it is invalid and you can display why
    return person, (req_courses, opt_courses), completed_topics, leftover_goals


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
