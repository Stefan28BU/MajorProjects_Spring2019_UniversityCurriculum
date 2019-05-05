from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('newCurriculum', views.newCurriculum, name='newCurriculum'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
