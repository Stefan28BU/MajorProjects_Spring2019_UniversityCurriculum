from django.db import models


class Person(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Person'


class Curriculum(models.Model):

    Cur_name = models.CharField(max_length=255, primary_key=True)
    Head_ID = models.ForeignKey(Person, on_delete=models.CASCADE)
    Min_Hours = models.PositiveIntegerField(default=0)

    extensive = 'EX'
    inclusive = 'IN'
    basicPlus = 'BP'
    basic = 'BC'
    unsatisfactory = 'US'
    substandard = 'SB'

    topicCategories = (
        (extensive, 'Extensive'),
        (inclusive, 'Inclusive'),
        (basicPlus, 'BasicPlus'),
        (basic, 'Basic'),
        (unsatisfactory, 'Unsatisfactory'),
        (substandard, 'Substandard'),
    )

    Topic_Category = models.CharField(max_length=255, choices=topicCategories, default=basic)

    class Meta:
        db_table = 'Curriculum'


class Course(models.Model):
    Subject_Code = models.CharField(max_length=255)
    Course_Number = models.CharField(max_length=255)
    Course_Name = models.CharField(max_length=255)
    Credit_Hours = models.PositiveIntegerField(default=0)
    Description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Course'

        constraints = [
            models.UniqueConstraint(fields=['Subject_Code', 'Course_Number'], name='course_unique')
        ]


class Topic(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

    class Meta:
        db_table = 'Topic'


class CourseTopics(models.Model):
    Course_Name = models.ForeignKey(Course, on_delete=models.CASCADE)
    Topic_ID = models.ForeignKey(Topic, on_delete=models.CASCADE)
    Units = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'CourseTopics'

        constraints = [
            models.UniqueConstraint(fields=['Course_Name', 'Topic_ID'], name='courseTopics_unique')
        ]


class CurriculumTopic(models.Model):

    lv1 = 1
    lv2 = 2
    lv3 = 3

    levels = (
        (lv1, 'Level 1'),
        (lv2, 'Level 2'),
        (lv3, 'Level 3'),
    )

    Cur_name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    ID = models.ForeignKey(CourseTopics, on_delete=models.CASCADE)
    Level = models.PositiveIntegerField(choices=levels, default=lv1)
    Subject_Area = models.CharField(max_length=255)
    Units = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'CurriculumTopic'
        constraints = [
            models.UniqueConstraint(fields=['ID', 'Cur_name'], name='currTopic_unique')
        ]


class Grade(models.Model):

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

    Grade_Distribution_ID = models.AutoField(primary_key=True)
    Grade = models.CharField(max_length=255, choices=grades)
    Person_ID = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Grade'
        constraints = [
            models.UniqueConstraint(fields=['Grade_Distribution_ID', 'Person_ID'], name='grade_unique')
        ]


class CourseSection(models.Model):
    spring = 'SP'
    summer = 'SM'
    fall = 'FA'
    winter = 'WI'

    semesters = (
        (spring, 'Spring semester'),
        (summer, 'Summer semester'),
        (fall, 'fall semester'),
        (winter, 'winter semester')
    )

    Section_ID = models.AutoField(primary_key=True)
    Course_Name = models.ForeignKey(Course, on_delete=models.CASCADE)
    Year = models.PositiveIntegerField(default=0)
    Semester = models.CharField(max_length=255, choices=semesters)
    Enrollment = models.CharField(max_length=255)
    Grade_Distribution_ID = models.ForeignKey(Grade, on_delete=models.CASCADE)
    Comment1 = models.CharField(max_length=255)
    Comment2 = models.CharField(max_length=255)

    class Meta:
        db_table = 'CourseSection'
        constraints = [
            models.UniqueConstraint(fields=['Section_ID', 'Course_Name', 'Year', 'Semester'],
                                    name='courseSection_unique')
        ]


class Goal(models.Model):
    ID = models.AutoField(primary_key=True)
    Cur_Name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    Description = models.CharField(max_length=255)
    Grade_Dist_ID = models.ForeignKey(Grade, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Goal'


class CourseGoal(models.Model):
    Goal_ID = models.ForeignKey(Goal, on_delete=models.CASCADE)
    Course_Name = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CourseGoal'
        constraints = [
            models.UniqueConstraint(fields=['Goal_ID', 'Course_Name'],
                                    name='courseGoal_unique')
        ]


class CurriculumCourse(models.Model):
    Cur_name = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    Course_Name = models.ForeignKey(Course, on_delete=models.CASCADE)
    Required = models.BooleanField()

    class Meta:
        db_table = 'CurriculumCourse'
        constraints = [
            models.UniqueConstraint(fields=['Cur_name', 'Course_Name'],
                                    name='curriculumCourse_unique')
        ]

