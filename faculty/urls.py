from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('create-classroom/', views.create_classroom_ajax, name='create_classroom_ajax'),
    path('join-classroom/', views.join_classroom_ajax, name='join_classroom_ajax'),
    path('get-classrooms/', views.get_classrooms_ajax, name='get_classrooms_ajax'),
    
    # ✅ URLs with classroom ID
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/<int:classroom_id>/upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('dashboard/', views.faculty_dashboard, name='dashboard'),
    path('repo/<int:submission_id>/', views.view_repo, name='view_repo'),
    path('repo/<int:submission_id>/download/', views.download_repo, name='download_repo'),
]
