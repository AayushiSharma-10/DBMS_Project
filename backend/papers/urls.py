from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Dashboards
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Paper actions
    path('upload/', views.upload, name='upload'),
    path('paper/<int:pk>/', views.detail, name='detail'),
    path('paper/<int:pk>/review/', views.review_paper, name='review_paper'),
]
