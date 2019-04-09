from django.forms import ModelForm
from ski.models import Mountain
from django import forms

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
