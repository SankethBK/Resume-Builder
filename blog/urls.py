from django.urls import path
from .views import homeView , PostDetailView , PostCreateView , PostUpdateView , PostDeleteView , UserPostListView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views 

urlpatterns = [
    path('',  homeView, name = 'blog-home'),
    path('user/<str:username>',UserPostListView.as_view() , name = 'user-posts'),
    path('post/<int:pk>',PostDetailView.as_view() , name = 'post-detail'),
    path('post/new/',PostCreateView.as_view() , name = 'post-create'),   
    path('post/<int:pk>/update/',PostUpdateView.as_view() , name = 'post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view() , name = 'post-delete'),
    path('about/', views.about , name = "blog-about"),
    path('search/', views.searchView, name = "search"),
    path('new/jobinvite/', views.createJobInvite, name = "jobinvite-new"),
    path('jobinvite/<int:id>/', views.jobInviteDetail, name = 'jobinvite-detail'),
    path('jobinvite/update/<int:id>/', views.jobinviteUpdate, name = "jobinvite-update"),
    path('jobinvite/delete/<int:id>/', views.jobInviteDeleteConfirm , name = "jobinvite-delete"),
    path('api/posts/', views.PostList.as_view()),
    path('apply/<int:jId>/', views.apply , name = "jobinvite-apply"),
    path('applicants/<int:id>/', views.viewApplicants, name = "jobinvite-applicants")
]