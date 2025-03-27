from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # Custom user model
    ROLE_CHOICES = (
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    # Additional fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
