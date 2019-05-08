from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import *

from .forms import *
from django.contrib import messages

from .dbFuncs.getInfo import *


def index(request):
    return render(request=request, template_name="index.html")


def newCurriculum(request):
    if request.method == 'POST':
        form = newCurriculumForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new curriculum.')
            form.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = newCurriculumForm()

    return render(request=request, template_name="curriculum/newCurriculum.html", context={"form": form})


def newHead(request):
    if request.method == 'POST':
        form = headForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new department head.')
            form.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = headForm()

    return render(request=request, template_name="curriculum/departmentHead.html", context={"form": form})


def newCourse(request):
    if request.method == 'POST':
        form = newCourseForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new curriculum.')
            form.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = newCourseForm()

    return render(request=request, template_name="curriculum/newCourse.html", context={"form": form})


def newTopic(request):
    if request.method == 'POST':
        form = newTopicForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new topic.')
            form.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = newTopicForm()

    return render(request=request, template_name="curriculum/newTopic.html", context={"form": form})


def newGoal(request):
    if request.method == 'POST':
        form = newGoalForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new goal.')
            form.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = newGoalForm()

    return render(request=request, template_name="curriculum/newGoal.html", context={"form": form})


def dashboard(request):
    curricula = Curriculum.objects.order_by('-Cur_name')[:5]
    output = ', '.join([c.Cur_name for c in curricula])
    return HttpResponse(output)


def editPerson(request):
    if request.method == 'POST':
        form = editPersonForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited person in charge.')
            temp = Person.objects.get(ID=form['curr'].value())

            temp.Name = form['name'].value()
            temp.save()

            print("person ", temp.Name)

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editPersonForm()

    return render(request=request, template_name="Edit/editPerson.html", context={"form": form})


def pickCuricToEdit(request):
    if request.method == 'POST':
        form = pickCuricToEditForm(request.POST)

        editMethod = form['editMethod'].value()
        print(editMethod)

        if editMethod == "edit":
            return HttpResponseRedirect('/Curriculum/editSpecificCurriculum/' + str(form['curr'].value()))
        elif editMethod == 'addCourse':
            return HttpResponseRedirect('/Curriculum/addCourseToCurric/' + str(form['curr'].value()))
        elif editMethod == 'editCourses':
            return HttpResponseRedirect('/Curriculum/selectCourseForCurricEdit/' + str(form['curr'].value()))
        elif editMethod == 'addTopic':
            return HttpResponseRedirect('/Curriculum/addTopicToCurriculum/' + str(form['curr'].value()))

    else:
        form = pickCuricToEditForm()
    return render(request=request, template_name="Edit/pickCurriculumToEdit.html", context={"form": form})


def pickCourseInCurriculumForEditing(request, curr_pk):
    if request.method == 'POST':
        form = pickCourseForCurricToEditForm(request.POST, curr_pk=curr_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited course in curriculum.')

            course_pk = form['courseToEdit'].value()
            editType = form['editType'].value()
            if editType == 'cct':
                return HttpResponseRedirect('/Curriculum/editCCT/'
                                            + str(curr_pk) + '/' + str(course_pk))
            else:
                return HttpResponseRedirect('/Curriculum/forkAddGradeCourseGoal/'
                                            + str(curr_pk) + '/' + str(course_pk))
        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = pickCourseForCurricToEditForm(curr_pk=curr_pk)

    return render(request=request, template_name="Edit/editCurriculum.html", context={"form": form})


def editCCT(request, curr_pk, course_pk):
    if request.method == 'POST':
        form = editCCTForm(request.POST, curr_pk=curr_pk, course_pk=course_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited cct.')

            units = form['units'].value()
            topic_pk = form['topic'].value()

            curric = Curriculum.objects.get(pk=curr_pk)
            course = Course.objects.get(pk=course_pk)
            topic = Topic.objects.get(pk=topic_pk)

            ct = CourseTopics.objects.get(Associated_Course=course, Associated_Topic=topic)
            cct = CurriculumCT.objects.get(Associated_CT=ct, Associated_Curriculum=curric)
            cct.Units = abs(int(units))
            cct.save()

            return HttpResponseRedirect('/Curriculum/editCurriculum')
        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editCCTForm(curr_pk=curr_pk, course_pk=course_pk)

    return render(request=request, template_name="Edit/editCourseInCurriculum.html", context={"form": form})


def addCourseToCurriculum(request, curr_pk):
    if request.method == 'POST':
        form = addCourseToCurricForm(request.POST, curr_pk=curr_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added course to curriculum.')

            course_pk = form['courseToAdd'].value()  # Get the course Primary Key from the page
            course = Course.objects.get(pk=course_pk)  # Get the course using the primary key
            course_topics = CourseTopics.objects.filter(Associated_Course=course)  # Get the CourseTopics of that course
            curric = Curriculum.objects.get(pk=curr_pk)  # Get the curriculum

            for ct in course_topics:
                cct = CurriculumCT(Associated_Curriculum=curric,
                                   Associated_CT=ct,
                                   Units=0)
                cct.save()
            # Create the necessary curriculum course topics

            curric_course = CurriculumCourse(Associated_Curriculum=curric,
                                             Associated_Course=course,
                                             Required=form['req'].value())
            curric_course.save()
            return HttpResponseRedirect('/Curriculum/editCurriculum/')

        else:
            messages.info(request, 'Failed to submit, form is invalid')

    else:
        form = addCourseToCurricForm(curr_pk=curr_pk)
    return render(request=request, template_name="Edit/addCourseToCurriculum.html", context={"form": form})


def editCurriculum(request, curr_id):
    if request.method == 'POST':
        form = editCurriculumForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited cucciculum.')

            temp = Curriculum.objects.get(pk=curr_id)
            tempPerson = Person.objects.get(ID=form['newHead'].value())

            temp.Head = tempPerson
            temp.Min_Hours = form['newHours'].value()

            temp.Percent_Level_2 = form['new_percent_2'].value()
            temp.Percent_Level_3 = form['new_percent_3'].value()

            temp.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editCurriculumForm()

    return render(request=request, template_name="Edit/editCurriculum.html", context={"form": form})


def gradeDist(request):
    if request.method == 'POST':
        form = gradeDistForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added grade distribution.')

            temp = Grade()

            temp.dist_number = form['dist'].value()
            temp.Letter_Grade = form['letterGrade'].value()
            temp.Associated_Course_Section = CourseSection.objects.get(Section_ID=form['section'].value())

            temp.save()


        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = gradeDistForm()

    return render(request=request, template_name="curriculum/gradeDist.html", context={"form": form})


def newSection(request):
    if request.method == 'POST':
        form = newSectionForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully added new section.')

            temp = CourseSection()

            temp.Semester = form['seme'].value()
            temp.Year = form['year'].value()
            temp.Comment1 = form['com1'].value()
            temp.Comment2 = form['com2'].value()
            temp.Enrollment = form['enroll'].value()
            temp.Associated_Course = Course.objects.get(pk=form['cName'].value())

            temp.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = newSectionForm()

    return render(request=request, template_name="curriculum/newSection.html", context={"form": form})


def editCourse(request, course_pk):
    if request.method == 'POST':
        form = editCourseForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited course.')

            temp = Course.objects.get(pk=course_pk)
            temp.Course_Number = form['newNum'].value()
            temp.Credit_Hours = form['newCred'].value()
            temp.Description = form['newDes'].value()
            temp.Course_Name = form['newName'].value()
            temp.Subject_Code = form['newCode'].value()
            temp.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editCourseForm()

    return render(request=request, template_name="Edit/editCourse.html", context={"form": form})


def editTopic(request):
    if request.method == 'POST':
        form = editTopicForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited topic.')

            temp = Topic.objects.get(ID=form['topic'].value())
            temp.Name = form['name'].value()

            temp.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editTopicForm()

    return render(request=request, template_name="Edit/editTopic.html", context={"form": form})


def editGoal(request):
    if request.method == 'POST':
        form = editGoalForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited goal.')

            tempGoal = Goal.objects.get(ID=form['goal'].value())
            tempGoal.Description = form['des'].value()

            tempCurr = Curriculum.objects.get(Cur_name=form['curr'].value())
            tempGoal.Associated_Curriculum = tempCurr
            tempGoal.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editGoalForm()

    return render(request=request, template_name="Edit/editGoal.html", context={"form": form})


def editSection(request):
    sec = CourseSection.objects.all()

    if request.method == 'POST':
        form = editSectionForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Successfully edited section.')

            tempSec = CourseSection.objects.get(Section_ID=form['currSection'].value())

            tempSec.Year = form['year'].value()
            tempSec.Semester = form['seme'].value()
            tempSec.Enrollment = form['enroll'].value()
            tempSec.Comment1 = form['com1'].value()
            tempSec.Comment2 = form['com2'].value()
            tempSec.save()

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = editSectionForm()

    return render(request=request, template_name="Edit/editSection.html", context={"form": form})


def qPage(request):
    return render(request=request, template_name="Queries/queryPage.html")


def q1(request):
    course_list = []
    topic_list = []
    if request.method == 'GET':
        form = queryOneForm(request.GET)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            curricula = form['curr'].value()

            course_list = get_courses_in_curricula(curricula)
            topic_list = get_topics_in_curricula(curricula)

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = queryOneForm()

    return render(request=request, template_name="Queries/q1.html",
                  context={"form": form, "course_list": course_list, "topic_list": topic_list})


def forkGoal(request, curr_pk, course_pk):
    if request.method == 'POST':
        form = forkGoalForm(request.POST)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            editMethod = form['editMethod'].value()
            if editMethod == 'grade':
                return HttpResponseRedirect('/Curriculum/gradeGoal/' + str(curr_pk) + '/'
                                            + str(course_pk))
            elif editMethod == 'add':
                return HttpResponseRedirect('/Curriculum/addGoalToCourse/' + str(curr_pk) + '/'
                                            + str(course_pk))

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = forkGoalForm()

    return render(request=request, template_name="Edit/forkForEditGoalsInCurriculum.html", context={"form": form})


def addGoalToCourse(request, curr_pk, course_pk):
    if request.method == 'POST':
        form = addGoalToCourseForm(request.POST, curr_pk=curr_pk, course_pk=course_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            course = Course.objects.get(pk=course_pk)
            goal_pk = form['goal'].value()
            goal = Goal.objects.get(pk=goal_pk)
            units = form['units'].value()
            cg = CourseGoal(Associated_Goal=goal, Associated_Course=course, Untis_Covered=units)
            cg.save()
            return HttpResponseRedirect('/Curriculum/editCurriculum')

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = addGoalToCourseForm(curr_pk=curr_pk, course_pk=course_pk)

    return render(request=request, template_name="Edit/forkForEditGoalsInCurriculum.html", context={"form": form})


def gradeGoal(request, curr_pk, course_pk):
    if request.method == 'POST':
        form = gradeGoalForm(request.POST, curr_pk=curr_pk, course_pk=course_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            course = Course.objects.get(pk=course_pk)
            goal_pk = form['goal'].value()
            grade = form['grade'].value()
            count = form['count'].value()

            goal = Goal.objects.get(pk=goal_pk)

            grades = Grade.objects.filter(Associated_Goal=goal, Letter_Grade = grade)

            if grades.count() > 0:
                grade_obj = Grade.objects.get(pk=grades[0].pk)
            else:
                grade_obj = Grade(Associated_Goal=goal, Letter_Grade=grade)
            grade_obj.dist_number = int(count)
            grade_obj.save()

            return HttpResponseRedirect('/Curriculum/editCurriculum')

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = gradeGoalForm(curr_pk=curr_pk, course_pk=course_pk)

    return render(request=request, template_name="Edit/forkForEditGoalsInCurriculum.html", context={"form": form})


def forkCourseManagement(request):
    if request.method == 'POST':
        form = pickCourseToManageForm(request.POST)

        editMethod = form['editMethod'].value()
        print(editMethod)

        if editMethod == 'edit':
            return HttpResponseRedirect('/Curriculum/editSpecificCourse/' + str(form['course'].value()))
        elif editMethod == 'addTopic':
            return HttpResponseRedirect('/Curriculum/addTopicToCourse/' + str(form['course'].value()))

    else:
        form = pickCourseToManageForm()
    return render(request=request, template_name="Edit/course/forkCourseEditPaths.html", context={"form": form})



def addTopicToCourse(request, course_pk):
    if request.method == 'POST':
        form = addTopicToCourseForm(request.POST, course_pk=course_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            course = Course.objects.get(pk=course_pk)
            topic_pk = form['topic'].value()

            topic = Topic.objects.get(pk=topic_pk)
            ct = CourseTopics(Associated_Course=course, Associated_Topic=topic)
            ct.save()
            ct = CourseTopics.objects.get(Associated_Course=ct.Associated_Course,
                                          Associated_Topic=ct.Associated_Topic)

            course_curric = CurriculumCourse.objects.filter(Associated_Course=course)
            for cc in course_curric:
                cct = CurriculumCT(
                    Associated_CT=ct,
                    Associated_Curriculum=cc.Associated_Curriculum
                )
                cct.save()

            return HttpResponseRedirect('/Curriculum/editCourse')

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = addTopicToCourseForm(course_pk=course_pk)

    return render(request=request, template_name="Edit/Course/addTopicToCourse.html", context={"form": form})


def q2(request):
    course_list = []
    curr_list = []
    if request.method == 'GET':
        form = queryTwoForm(request.GET)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            course = form['course'].value()

            q2obj = get_info_on_course_with_name(course)

            course_list = q2obj[0]
            curr_list = q2obj[1]

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = queryTwoForm()

    return render(request=request, template_name="Queries/q2.html",
                  context={"form": form, "course_list": course_list, "curr_list": curr_list})


def q3(request):
    sec_list = []
    list_list = []
    sec_list1 = []
    list_list1 = []

    if request.method == 'GET':
        form = queryThreeForm(request.GET)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            course = form['course'].value()
            curr = form['curr'].value()
            startSem = form['startSem'].value()
            endSem = form['endSem'].value()
            startYear = form['startYear'].value()
            endYear = form['endYear'].value()

            if startYear == '' and endYear == '':
                q3obj = get_info_on_course_no_range(course, curr)
                sec_list = q3obj[1]
                grade_dist = q3obj[0]

                for sec in sec_list:
                    gList = []

                    for g, count in grade_dist[str(sec.pk)].items():
                        gList.append(str(g) + ': ' + str(count) + ' students')
                    list_list.append(('Without range: ', sec, gList))
            else:
                q3obj = get_sections_grades_of_a_course_with_range(course, curr, startSem, startYear,
                                                                   endSem,
                                                                   endYear)
                sec_list = q3obj[1]
                grade_dist = q3obj[0]

                for sec in sec_list:
                    gList = []

                    for g, count in grade_dist[str(sec.pk)].items():
                        gList.append(str(g) + ': ' + str(count) + ' students')
                    list_list.append(('With range: ', sec, gList))

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = queryThreeForm()

    return render(request=request, template_name="Queries/q3.html",
                  context={"form": form, "sec_list": sec_list, "list_list": list_list})


def addTopicToCurric(request, curr_pk):
    if request.method == 'POST':
        form = addTopicToCurricForm(request.POST, curr_pk=curr_pk)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            topic_pk = form['topic'].value()
            topic = Topic.objects.get(pk=topic_pk)
            curric = Curriculum.objects.get(pk=curr_pk)

            level = form['level'].value()
            sub_area = form['subject_area'].value()
            units = form['units'].value()

            ct = CurriculumTopic(Associated_Topic=topic, Associated_Curriculum=curric,
                                 Level=level, Subject_Area=sub_area, Units=units)
            ct.save()
            return HttpResponseRedirect('/Curriculum/editCurriculum/')

        else:
            messages.info(request, 'Failed to submit, form is invalid')

    else:
        form = addTopicToCurricForm(curr_pk=curr_pk)
    return render(request=request, template_name="Edit/createCurriculumTopic.html", context={"form": form})


def q4(request):
    grade_dist = []
    sec_list = []
    list_list = []

    if request.method == 'GET':
        form = queryFourForm(request.GET)

        if form.is_valid():
            messages.add_message(request, messages.INFO, 'Success.')

            curr = form['curr'].value()
            startSem = form['startSem'].value()
            endSem = form['endSem'].value()
            startYear = form['startYear'].value()
            endYear = form['endYear'].value()

            startC = form['startCoursenum'].value()
            endC = form['endCoursenum'].value()


            if startC == '' and endC == '':
                q4obj = get_sections_in_a_cur_with_time_range(curr, startSem, startYear, endSem, endYear)

                grade_dist = q4obj[0]
                sec_list = q4obj[1]

            else:
                q4obj = get_sections_in_a_cur_with_time_range_and_course_range(curr, startSem, startYear, endSem, endYear, startC, endC)

                grade_dist = q4obj[0]
                sec_list = q4obj[1]

            for secL in sec_list:
                for sec in secL:
                    gList = []

                    for g, count in grade_dist[str(sec.pk)].items():
                        gList.append((g, count))
                    list_list.append(('Without range: ', sec, gList))


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

            for a, b, gList in list_list:
                for grade, count in gList:
                    gradeDict[grade] += count

            tot_grade_list = []
            for grade, count in gradeDict.items():
                tot_grade_list.append( grade + ': ' + str(count) )

        else:
            print('Invalid')
            messages.info(request, 'Failed to submit, form is invalid')
    else:
        form = queryFourForm()

    return render(request=request, template_name="Queries/q4.html",
                  context={"form": form, "sec_list": sec_list, "list_list": list_list,
                           "tot_grade_list": tot_grade_list})


def q5(request):

    if request.method == 'GET':
        form = queryFiveForm(request.GET)
    else:
        form = queryFiveForm()

    result = set()
    for c in Curriculum.objects.all():
        person, course_tuple, topic_tuple, goal_tuple, top_cat, goal_validity  = q5_ryland_style(c)
        result.add((c, person, str(course_tuple[0]), str(course_tuple[1]), tuple(topic_tuple[0]),
                    tuple(topic_tuple[1]), tuple(goal_tuple[0]), tuple(goal_tuple[1]), top_cat, str(goal_validity)))
        # 0 - Curriculum                            -   Curriculum
        # 1 - Person                                -   Person
        # 2 - Required courses                      -   Number
        # 3 - Optional Courses                      -   Number
        # 4 - Covered topics                        -   (CurriculumTopic, Num)  - list
        # 5 - Not covered by requirements topics    -   CurriculumTopic         - list
        # 6 - Valid goals                           -   Goal                    - list
        # 7 - Invalid Goals                         -   Goal                    - list
        # 8 - Topic Category                        -   String
        # 9 - Goal Validity                         -   String


    return render(request=request, template_name="Queries/q5.html",
                  context={"form": form, "ret": result})
