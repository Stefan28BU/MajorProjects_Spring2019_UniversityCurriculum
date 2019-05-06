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

	# path('editSection/', views.editSection, name='editSection'),
    path('editTopic/', views.editTopic, name='editTopic'),
    path('editGoal/', views.editGoal, name='editGoal'),

]
