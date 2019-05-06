from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newCurriculum/', views.newCurriculum, name='newCurriculum'),
    path('departmentHead/', views.newHead, name='departmentHead'),
    path('newCourse/', views.newCourse, name='newCourse'),
    path('newTopic/', views.newTopic, name='newTopic'),
    path('newGoal/', views.newGoal, name='newGoal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editPerson/', views.editPerson, name='editPerson'),
    path('editCurriculum/', views.pickCuricToEdit, name='editCurriculum'),
    path('gradeDist/', views.gradeDist, name='gradeDist'),
    path('newSection/', views.newSection, name='newSection'),
    path('editCourse/', views.editCourse, name='editCourse'),
    path('editSpecificCurriculum/<int:curr_id>', views.editCurriculum, name='editSpecificCurriculum'),
    path('addCourseToCurric/<int:curr_pk>', views.addCourseToCurriculum, name='addCourseToCurriculum'),
    path('selectCourseForCurricEdit/<int:curr_pk>', views.pickCourseInCurriculumForEditing,
         name='selectCourseForCurricEdit'),
    path('editCCT/<int:curr_pk>/<int:course_pk>', views.editCCT, name='editCCT'),
    path('forkAddGradeCourseGoal/<int:curr_pk>/<int:course_pk>', views.forkGoal, name='forkAddGradeCourseGoal'),
    path('addGoalToCourse/<int:curr_pk>/<int:course_pk>', views.addGoalToCourse, name='addGoalToCourse'),


	path('editSection/', views.editSection, name='editSection'),
    path('editTopic/', views.editTopic, name='editTopic'),
    path('editGoal/', views.editGoal, name='editGoal'),

]
