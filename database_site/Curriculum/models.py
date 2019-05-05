from django.db import models


class Person(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)

    def __str__(self):
	    return str(self.ID) + ' ' + self.Name

    class Meta:
	    db_table = 'Person'






class Curriculum(models.Model):
    Cur_name = models.CharField(max_length=255, primary_key=True)
    Head = models.ForeignKey(Person, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.Cur_name

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
    Associated_Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Associated_Topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    Units = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'CourseTopics'

        constraints = [
            models.UniqueConstraint(fields=['Associated_Course', 'Associated_Topic'], name='courseTopics_unique')
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

    Associated_Curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    Associated_Topic = models.ForeignKey(CourseTopics, on_delete=models.CASCADE)
    Level = models.PositiveIntegerField(choices=levels, default=lv1)
    Subject_Area = models.CharField(max_length=255)
    Units = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'CurriculumTopic'
        constraints = [
            models.UniqueConstraint(fields=['Associated_Curriculum', 'Associated_Topic'], name='currTopic_unique')
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
    Associated_Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Year = models.PositiveIntegerField(default=0)
    Semester = models.CharField(max_length=255, choices=semesters)
    Enrollment = models.CharField(max_length=255)
    Comment1 = models.CharField(max_length=255)
    Comment2 = models.CharField(max_length=255)

    class Meta:
        db_table = 'CourseSection'
        constraints = [
            models.UniqueConstraint(fields=['Section_ID', 'Associated_Course', 'Year', 'Semester'],
                                    name='courseSection_unique')
        ]


class Goal(models.Model):
    ID = models.AutoField(primary_key=True)
    Associated_Curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    Description = models.CharField(max_length=255)

    class Meta:
        db_table = 'Goal'


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
    Letter_Grade = models.CharField(max_length=255, choices=grades)
    Associated_Course_Section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, null=True)
    Associated_Goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True)
    dist_number = models.IntegerField(default=0)


    class Meta:
        db_table = 'Grade'


class CourseGoal(models.Model):
    Associated_Goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    Associated_Course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        db_table = 'CourseGoal'
        constraints = [
            models.UniqueConstraint(fields=['Associated_Goal', 'Associated_Course'],
                                    name='courseGoal_unique')
        ]


class CurriculumCourse(models.Model):
    Associated_Curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    Associated_Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    Required = models.BooleanField()

    class Meta:
        db_table = 'CurriculumCourse'
        constraints = [
            models.UniqueConstraint(fields=['Associated_Curriculum', 'Associated_Course'],
                                    name='curriculumCourse_unique')
        ]
