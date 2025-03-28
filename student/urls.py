from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),  # ✅ Unified dashboard
    path('join-classroom/', views.join_classroom, name='join_classroom'),  # ✅ Join classroom
    path('upload-submission/', views.upload_submission, name='upload_submission'),  # ✅ Upload submission
    path('submit-github/', views.submit_github_repo, name='submit_github_repo'),
]
