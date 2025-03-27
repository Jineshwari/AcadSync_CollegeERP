from django import forms
from accounts.models import User

# ✅ Form for editing faculty profile
class EditFacultyProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'profile_photo']

from django import forms
from .models import Classroom

# ✅ Classroom Creation Form
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'description']
