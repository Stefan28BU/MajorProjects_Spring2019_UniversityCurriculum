from django import forms

from .models import *

from django import forms


class headForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = "__all__"

        labels = {
            'Name': 'Your Name'
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class newCurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum

        Percent_Level_2 = forms.IntegerField(min_value=0, max_value=100, label='Percent of level 2 topics needed for categorization', widget=forms.TextInput(attrs={'class': 'selectpicker form-control'}))
        Percent_Level_3 = forms.IntegerField(min_value=0, max_value=100, label='Percent of level 3 topics needed for categorization', widget=forms.TextInput(attrs={'class': 'selectpicker form-control'}))

        fields = ['Head', 'Cur_name', 'Min_Hours', 'Percent_Level_2', 'Percent_Level_3']

        labels = {
            'Cur_name': 'Curriculum Name',
            'Min_Hours': 'Minimum Hours',
            'Head': 'Curriculum Head',
            'Percent_Level_2': 'Percent of level 2 topics needed for categorization',
            'Percent_Level_3': 'Percent of level 3 topics needed for categorization',
        }
        widgets = {
            'Head': forms.Select(attrs={'class': 'selectpicker form-control'}),

            'Cur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'Min_Hours': forms.TextInput(attrs={'class': 'form-control'}),
        }


class editPersonForm(forms.Form):
    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    curr = forms.ChoiceField(choices=pChoices, label="Select a Department Head",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}), label="New Name")


class pickCuricToEditForm(forms.Form):
    cTupleArray = []
    for c in Curriculum.objects.all():
        cTupleArray.append((c.pk, 'Curriculum: ' + c.Cur_name + ', Head: ' + c.Head.Name + '(' + str(
            c.Head.ID) + '), Minimum Hours: ' + str(c.Min_Hours)))
    cChoices = tuple(cTupleArray)

    curr = forms.ChoiceField(choices=cChoices, label="Select a Curriculum",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    editChoices = (
        ('edit', 'Edit the general info'),
        ('removeCourse', 'Remove a Course'),
        ('addCourse', 'Add a Course'),
        ('editCourses', 'Manage Courses'),
        ('addTopic', 'Add a Topic to the Curriculum'),
    )
    editMethod = forms.ChoiceField(choices=editChoices, label="What would you like to do",
                                   widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class editCurriculumForm(forms.Form):
    pTupleArray = []
    for p in Person.objects.all():
        pTupleArray.append((p.ID, p.Name + ' ' + str(p.ID)))
    pChoices = tuple(pTupleArray)

    newHead = forms.ChoiceField(choices=pChoices, label="Select a New Head",
                                widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    newHours = forms.IntegerField(initial=0, label="Enter New Credit Hours",
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    new_percent_2 = forms.IntegerField(min_value=0, max_value=100, label="Percentage of level 2 topics needed")
    new_percent_3 = forms.IntegerField(min_value=0, max_value=100, label="Percentage of level 3 topics needed")


class addCourseToCurricForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.curr_pk = kwargs.pop('curr_pk')
        super(addCourseToCurricForm, self).__init__(*args, **kwargs)

        courses = Course.objects.all()

        curric = Curriculum.objects.get(pk=self.curr_pk)
        course_already_added = set()
        for cc in CurriculumCourse.objects.filter(Associated_Curriculum=curric):
            course_already_added.add(cc.Associated_Course)

        coursesSet = set(courses) - course_already_added

        cTupleArray = set()
        for c in coursesSet:
            cTupleArray.add((c.pk, c.Subject_Code + ' ' + c.Course_Number + ': ' + c.Course_Name))
        cChoices = tuple(cTupleArray)

        self.fields['courseToAdd'] = forms.ChoiceField(choices=cChoices, label="Select the course to add",
                                                       widget=forms.Select(
                                                           attrs={'class': 'selectpicker form-control'}))
        self.fields['req'] = forms.BooleanField(label="Required")


# At this point, just have a drop down to pick the course
# Have that automatically create the CC and whatever CCT's are needed
# In the pick... form, add an option to edit course info
# Have that bring you to a page where you pick the course
# Have THAT bring you to a page where you can edit the CCT
#


class pickCourseForCurricToEditForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.curr_pk = kwargs.pop('curr_pk')
        super(pickCourseForCurricToEditForm, self).__init__(*args, **kwargs)

        curric = Curriculum.objects.get(pk=self.curr_pk)
        curric_courses = CurriculumCourse.objects.filter(Associated_Curriculum=curric)
        course_choices = set()
        for cc in curric_courses:
            course_choices.add((cc.Associated_Course.pk,
                                cc.Associated_Course.Subject_Code + ' '
                                + str(cc.Associated_Course.Course_Number)))

        self.fields['courseToEdit'] = forms.ChoiceField(choices=course_choices, label="Select the course to edit",
                                                        widget=forms.Select(
                                                            attrs={'class': 'selectpicker form-control'}))
        edit_choices = (
            ('cct', "Topics in the Course"),
            ('goal', "Goals for the Course"),
        )
        self.fields['editType'] = forms.ChoiceField(choices=edit_choices, label="What to edit",
                                                    widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class editCCTForm(forms.Form):
    def __init__(self, *args, **kwargs):
        curr_pk = kwargs.pop('curr_pk')
        course_pk = kwargs.pop('course_pk')
        super(editCCTForm, self).__init__(*args, **kwargs)

        course = Course.objects.get(pk=course_pk)
        curric = Curriculum.objects.get(pk=curr_pk)
        ct_of_course = CourseTopics.objects.filter(Associated_Course=course)
        cct_of_curriculum = CurriculumCT.objects.filter(Associated_Curriculum=curric,
                                                        Associated_CT__in=ct_of_course)

        # Get course, curriculum
        # Get the courseTopics of the course
        # Get the curricCT of the curriculum, where they point to a ct of the course

        topic_choices = set()
        for cct in cct_of_curriculum:
            t = cct.Associated_CT.Associated_Topic
            topic_choices.add((t.pk, t.Name))

        self.fields['topic'] = forms.ChoiceField(choices=topic_choices, label="Topic to edit",
                                                 widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
        self.fields['units'] = forms.IntegerField(label="Units", min_value=0)


class newGoalForm(forms.ModelForm):
    class Meta:
        model = Goal

        fields = ['Associated_Curriculum', 'Description', 'Units_For_Completion']

        labels = {
            'Associated_Curriculum': 'Curriculum',
            'Description': 'Description',
            'Units_For_Completion': 'Units needed to complete'
        }

        widgets = {
            'Associated_Curriculum': forms.Select(attrs={'class': 'selectpicker form-control'}),

            'Description': forms.TextInput(attrs={'class': 'form-control'}),
            'Units_For_Completion': forms.IntegerField(min_value=0),
        }


class newCourseForm(forms.ModelForm):
    class Meta:
        model = Course

        fields = ['Subject_Code', 'Course_Number', 'Course_Name', 'Credit_Hours', 'Description']

        labels = {
            'Subject_Code': 'Subject Code',
            'Course_Number': 'Course Number',
            'Course_Name': 'Course Name',
            'Credit_Hours': 'Credit Hours',
            'Description': 'Description'
        }

        widgets = {
            'Subject_Code': forms.TextInput(attrs={'class': 'form-control'}),
            'Course_Number': forms.TextInput(attrs={'class': 'form-control'}),
            'Course_Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Credit_Hours': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': forms.TextInput(attrs={'class': 'form-control'}),
        }


class newTopicForm(forms.ModelForm):
    class Meta:
        model = Topic

        fields = ['Name']

        labels = {
            'Name': 'Topic Name'
        }

        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class gradeDistForm(forms.Form):
    AP = 'A+'
    A = 'A'
    AM = 'A-'
    BP = 'B+'
    B = 'B'
    BM = 'B-'
    CP = 'C+'
    C = 'C'
    CM = 'C-'
    DP = 'D+'
    D = 'D'
    DM = 'D-'
    F = 'F'
    W = 'W'
    I = 'I'

    grades = (
        (AP, 'A+'),
        (A, 'A'),
        (AM, 'A-'),
        (BP, 'B+'),
        (B, 'B'),
        (BM, 'B-'),
        (CP, 'C+'),
        (C, 'C'),
        (CM, 'C-'),
        (DP, 'D+'),
        (D, 'D'),
        (DM, 'D-'),
        (F, 'Fail'),
        (W, 'Withdraw'),
        (I, 'Incomplete')
    )

    letterGrade = forms.ChoiceField(choices=grades, label="Select a Grade",
                                    widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    dist = forms.IntegerField(initial=0, label="Enter Number of Students",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    secTupleArray = []
    for s in CourseSection.objects.all():
        spring = 'SP'
        summer = 'SM'
        fall = 'FA'
        winter = 'WI'
        sem = ''

        if s.Semester == spring:
            sem = 'Spring'

        elif s.Semester == summer:
            sem = 'Summer'

        elif s.Semester == fall:
            sem = 'Fall'

        elif s.Semester == winter:
            sem = 'Winter'

        secTupleArray.append((s.Section_ID, 'Course: ' + s.Associated_Course.Course_Name + ', Section: ' + sem + ' ' + str(s.Year) + 'Section ID: ' + str(s.Section_ID)))

    secChoice = tuple(secTupleArray)

    section = forms.ChoiceField(choices=secChoice, label="Choose a Section",
                                widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class gradeGoalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        curr_pk = kwargs.pop('curr_pk')
        course_pk = kwargs.pop('course_pk')

        super(gradeGoalForm, self).__init__(*args, **kwargs)

        # Display Goals associated with course

        course = Course.objects.get(pk=course_pk)
        course_goals = CourseGoal.objects.filter(Associated_Course=course)
        goal_choices = set()
        for cg in course_goals:
            goal_choices.add((cg.Associated_Goal.pk, cg.Associated_Goal.Description))


        self.fields['goal'] = forms.ChoiceField(choices=goal_choices, label="Goal to Grade",
                                                widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

        AP = 'A+'
        A = 'A'
        AM = 'A-'
        BP = 'B+'
        B = 'B'
        BM = 'B-'
        CP = 'C+'
        C = 'C'
        CM = 'C-'
        DP = 'D+'
        D = 'D'
        DM = 'D-'
        F = 'F'
        W = 'W'
        I = 'I'

        grades = (
            (AP, 'A+'),
            (A, 'A'),
            (AM, 'A-'),
            (BP, 'B+'),
            (B, 'B'),
            (BM, 'B-'),
            (CP, 'C+'),
            (C, 'C'),
            (CM, 'C-'),
            (DP, 'D+'),
            (D, 'D'),
            (DM, 'D-'),
            (F, 'Fail'),
            (W, 'Withdraw'),
            (I, 'Incomplete')
        )


        self.fields['grade'] = forms.ChoiceField(choices=grades, label="Level of the topic",
                                                 widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

        self.fields['count'] = forms.IntegerField(label="Count", min_value=0)






class newSectionForm(forms.Form):
    TupleArray = []
    for g in Course.objects.all():
        TupleArray.append((g.pk, 'Course: ' + g.Subject_Code + g.Course_Number + ' (' + g.Course_Name + ')'))

    gChoice = tuple(TupleArray)

    cName = forms.ChoiceField(choices=gChoice, label="Choose a Course",
                              widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    year = forms.IntegerField(initial=0, label="Enter a Year", widget=forms.TextInput(attrs={'class': 'form-control'}))

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring'),
        (summer, 'Summer'),
        (fall, 'Fall'),
        (winter, 'Winter')
    )

    seme = forms.ChoiceField(choices=semesters, label="Choose a Semester",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    enroll = forms.IntegerField(initial=0, label="Enter Number of Enrollment",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    com1 = forms.CharField(max_length=255, label="Enter First Comment",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    com2 = forms.CharField(max_length=255, label="Enter Second Comment",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class editCourseForm(forms.Form):
    newName = forms.CharField(max_length=255, label="Enter New Name",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    newCode = forms.CharField(max_length=255, label="Enter New Subject Code",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    newNum = forms.CharField(max_length=255, label="Enter New Course Number",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    newCred = forms.IntegerField(initial=0, label="Enter New Hours",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    newDes = forms.CharField(max_length=255, label="Enter New Description",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))


class editTopicForm(forms.Form):
    tpTupleArray = []
    for g in Topic.objects.all():
        tpTupleArray.append((g.ID, g.Name))

    tpChoice = tuple(tpTupleArray)

    topic = forms.ChoiceField(choices=tpChoice, label="Choose a Topic",
                              widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    name = forms.CharField(max_length=255, label="Enter New Topic Name",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class editGoalForm(forms.Form):
    goalTupleArray = []
    for g in Goal.objects.all():
        goalTupleArray.append((g.ID, g.Description))

    goalChoice = tuple(goalTupleArray)

    goal = forms.ChoiceField(choices=goalChoice, label="Choose a Goal",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    des = forms.CharField(max_length=255, label="Enter New Description",
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    units = forms.IntegerField(label='Units for Completion', min_value=0)


    currTupleArray = []
    for c in Curriculum.objects.all():
        currTupleArray.append((c.Cur_name, 'Curriculum: ' + c.Cur_name + ', Head: ' + c.Head.Name + '(' + str(
            c.Head.ID) + '), Minimum Hours: ' + str(c.Min_Hours)))

    currChoice = tuple(currTupleArray)

    curr = forms.ChoiceField(choices=currChoice, label="Choose a Curriculum",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


# Get Grade or add
class forkGoalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forkGoalForm, self).__init__(*args, **kwargs)

        choices = (
            ('grade', 'Grade a Goal'),
            ('add', 'Add a new Goal to the Course')
        )

        self.fields['editMethod'] = forms.ChoiceField(choices=choices, label="Topic to edit",
                                                      widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class addGoalToCourseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        curr_pk = kwargs.pop('curr_pk')
        course_pk = kwargs.pop('course_pk')

        super(addGoalToCourseForm, self).__init__(*args, **kwargs)

        # Display Goals associated with curriculum, not associated with course

        curric = Curriculum.objects.get(pk=curr_pk)
        course = Course.objects.get(pk=course_pk)
        curr_goals = Goal.objects.filter(Associated_Curriculum=curric)
        course_cg = CourseGoal.objects.filter(Associated_Course=course)
        already_goals = set()
        for cg in course_cg:
            already_goals.add(cg.Associated_Goal)

        new_goals = set(curr_goals) - already_goals

        choices = set()
        for g in new_goals:
            choices.add((g.pk, g.Description))

        self.fields['goal'] = forms.ChoiceField(choices=choices, label="Goal to add",
                                                widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
        self.fields['units'] = forms.IntegerField(label='Untis covered in course', min_value=0)


class editSectionForm(forms.Form):
    secTupleArray = []
    for s in CourseSection.objects.all():
        spring = 'SP'
        summer = 'SM'
        fall = 'FA'
        winter = 'WI'
        sem = ''

        if s.Semester == spring:
            sem = 'Spring'

        elif s.Semester == summer:
            sem = 'Summer'

        elif s.Semester == fall:
            sem = 'Fall'

        elif s.Semester == winter:
            sem = 'Winter'

        secTupleArray.append(
            (s.Section_ID, s.Associated_Course.Course_Name + ' (' + sem + ' ' + str(s.Year) + '), Section '  + str(s.Section_ID)))

    secChoice = tuple(secTupleArray)

    currSection = forms.ChoiceField(choices=secChoice, label="Choose a Section",
                                    widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    year = forms.IntegerField(initial=0, label="Enter New Year",
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring'),
        (summer, 'Summer'),
        (fall, 'Fall'),
        (winter, 'Winter')
    )

    seme = forms.ChoiceField(choices=semesters, label="Choose a New Semester",
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    enroll = forms.IntegerField(initial=0, label="Enter New Enrollment Number",
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    com1 = forms.CharField(max_length=255, label="Enter First Comment",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    com2 = forms.CharField(max_length=255, label="Enter Second Comment",
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class queryOneForm(forms.Form):
    pTupleArray = []
    for p in Curriculum.objects.all():
        pTupleArray.append((p.Cur_name, p.Cur_name))
    pChoices = tuple(pTupleArray)

    curr = forms.ChoiceField(choices=pChoices, label="Select a Curriculum", required=False,
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class queryTwoForm(forms.Form):
    pTupleArray = []
    for p in Course.objects.all():
        pTupleArray.append((p.Course_Name, p.Subject_Code + ' ' + p.Course_Number + ' (' + p.Course_Name + ')'))
    pChoices = tuple(pTupleArray)

    course = forms.ChoiceField(choices=pChoices, label="Select a Course", required=False,
                               widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class queryThreeForm(forms.Form):
    pTupleArray = []
    for p in Course.objects.all():
        pTupleArray.append((p.Course_Name, p.Subject_Code + ' ' + p.Course_Number + ' (' + p.Course_Name + ')'))
    pChoices = tuple(pTupleArray)

    course = forms.ChoiceField(choices=pChoices, label="Select a Course", required=False,
                               widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    curTupleArray = []
    for p in Curriculum.objects.all():
        curTupleArray.append((p.Cur_name, p.Cur_name))
    currChoices = tuple(curTupleArray)

    curr = forms.ChoiceField(choices=currChoices, label="Select a Curriculum", required=False,
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring'),
        (summer, 'Summer'),
        (fall, 'Fall'),
        (winter, 'Winter')
    )

    startYear = forms.IntegerField(initial=0, label="From",
                                   widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    startSem = forms.ChoiceField(choices=semesters, label="Choose a Semester",
                                 widget=forms.Select(attrs={'class': 'selectpicker form-control'}), required=False)

    endYear = forms.IntegerField(initial=0, label="To",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    endSem = forms.ChoiceField(choices=semesters, label="Choose a Semester",
                               widget=forms.Select(attrs={'class': 'selectpicker form-control'}), required=False)


class queryFourForm(forms.Form):
    curTupleArray = []
    for p in Curriculum.objects.all():
        curTupleArray.append((p.Cur_name, p.Cur_name))
    currChoices = tuple(curTupleArray)

    curr = forms.ChoiceField(choices=currChoices, label="Select a Curriculum",required=False,
                             widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring'),
        (summer, 'Summer'),
        (fall, 'Fall'),
        (winter, 'Winter')
    )

    startYear = forms.IntegerField(initial=0, label="From",required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))

    startSem = forms.ChoiceField(choices=semesters, label="Choose a Semester",required=False,
                                 widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    endYear = forms.IntegerField(initial=0, label="To",required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))

    endSem = forms.ChoiceField(choices=semesters, label="Choose a Semester",required=False,
                               widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

    startCoursenum = forms.IntegerField(initial=0, label="From Course Number", required=False,
                               widget=forms.TextInput(attrs={'class': 'selectpicker form-control'}))

    endCoursenum = forms.IntegerField(initial=0, label="From Course Number", required=False,
                                    widget=forms.TextInput(attrs={'class': 'selectpicker form-control'}))


class pickCourseToManageForm(forms.Form):
    cTupleArray = []
    for c in Course.objects.all():
        cTupleArray.append((c.pk, c.Subject_Code + ' ' + c.Course_Number))
    cChoices = tuple(cTupleArray)

    course = forms.ChoiceField(choices=cChoices, label="Select a Course",
                               widget=forms.Select(attrs={'class': 'selectpicker form-control'}))
    editChoices = (
        ('edit', 'Edit the general info'),
        ('addTopic', 'Add a Topic'),
    )
    editMethod = forms.ChoiceField(choices=editChoices, label="What would you like to do",
                                   widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class addTopicToCourseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        course_pk = kwargs.pop('course_pk')

        super(addTopicToCourseForm, self).__init__(*args, **kwargs)

        # Display Goals associated with curriculum, not associated with course

        course = Course.objects.get(pk=course_pk)
        all_topics = Topic.objects.all()
        already_course_topics = CourseTopics.objects.filter(Associated_Course=course)
        already_topics = set()
        for ct in already_course_topics:
            already_topics.add(ct.Associated_Topic)

        new_topics = set(all_topics) - already_topics
        choices = set()
        for t in new_topics:
            choices.add((t.pk, t.Name))

        self.fields['topic'] = forms.ChoiceField(choices=choices, label="Topic to add",
		                                         widget=forms.Select(attrs={'class': 'selectpicker form-control'}))


class addTopicToCurricForm(forms.Form):
    def __init__(self, *args, **kwargs):
        curr_pk = kwargs.pop('curr_pk')

        super(addTopicToCurricForm, self).__init__(*args, **kwargs)

        # Display Goals associated with curriculum, not associated with course

        curric = Curriculum.objects.get(pk=curr_pk)

        all_topics = Topic.objects.all()
        already_curric_topics = CurriculumTopic.objects.filter(Associated_Curriculum=curric)
        already_topics = set()
        for ct in already_curric_topics:
            already_topics.add(ct.Associated_Topic)
        topics = set(all_topics) - already_topics

        topic_choices = set()
        for t in topics:
            topic_choices.add((t.pk, t.Name))

        self.fields['topic'] = forms.ChoiceField(choices=topic_choices, label="Topic to add",
		                                         widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

        level_choices = (
            (1, '1'),
            (2, '2'),
            (3, '3'),
        )
        self.fields['level'] = forms.ChoiceField(choices=level_choices, label="Level of the topic",
		                                         widget=forms.Select(attrs={'class': 'selectpicker form-control'}))

        self.fields['subject_area'] = forms.CharField(label="Enter the subject area")
        self.fields['units'] = forms.IntegerField(label="Units", min_value=0)



class queryFiveForm(forms.Form):
    x = 3
