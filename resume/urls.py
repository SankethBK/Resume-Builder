from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_home , name = 'resume-home'),
    path('choose-template/' , views.chooseTemplate , name = "choose-template"),
    path('details/<int:id>' , views.details , name = 'resume-details'),
    path('complete/', views.complete , name = 'resume-complete')
]