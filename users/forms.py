from django.contrib.auth.models import Group
from django import forms

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "permissions"]