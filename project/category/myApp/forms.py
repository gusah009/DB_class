from django import forms
from .models import Students

class PostForm(forms.ModelForm):
  
  class Meta:

    model = Students
    fields = ['id', 'firstname', 'secondname', 'age', 'major', 'address']