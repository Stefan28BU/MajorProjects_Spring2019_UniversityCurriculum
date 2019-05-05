from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newCurriculum/', views.newCurriculum, name='newCurriculum'),
    path('departmentHead/', views.newHead, name='departmentHead'),
    path('newCourse/', views.newCourse, name='newCourse'),
    path('newTopic/', views.newTopic, name='newTopic'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
