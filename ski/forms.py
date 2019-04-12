from django import forms
from django.forms import ModelForm

from ski.models import Mountain


class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
