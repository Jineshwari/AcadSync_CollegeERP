# student/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .models import StudentProfile

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Create StudentProfile on user creation."""
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=UserSocialAuth)
def save_github_username(sender, instance, **kwargs):
    """Save GitHub username to StudentProfile."""
    if instance.provider == 'github':
        user = instance.user
        profile, created = StudentProfile.objects.get_or_create(user=user)
        profile.github_username = instance.extra_data.get('login')  # GitHub username
        profile.save()
