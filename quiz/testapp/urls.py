from django.contrib import admin
from django.urls import path
from testapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('',views.index,name='index'),
    path('HandleLogin',views.HandleLogin,name='HandleLogin'),
    path('HandleLogout',views.HandleLogout,name='HandleLogout'),
    path('Profile',views.Profile,name='Profile'),
    path('Createquiz',views.Createquiz,name='Createquiz'),
    path('AllQuestions',views.viewQuestions,name='viewQuestions'),
    path('UpdateQuestion/<pk>',views.UpdateQuestion,name='UpdateQuestion'),
    path('DeleteQuestion/<pk>',views.DeleteQuestion,name='DeleteQuestion'),
    path('ConfirmUpdate',views.ConfirmUpdate,name='ConfirmUpdate'),
    path('Settime',views.Settime,name='Settime'),
    path('attempt/<s_pk>',views.attempt,name='attempt'),
    path('Submit',views.Submit,name='Submit'),
]