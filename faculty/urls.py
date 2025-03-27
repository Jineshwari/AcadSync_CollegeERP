from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('profile/', views.faculty_profile, name='faculty_profile'),  # Faculty profile
    path('profile/edit/', views.edit_faculty_profile, name='edit_faculty_profile'),  # Edit profile
    path('create-classroom/', views.create_classroom, name='create_classroom'),
]
