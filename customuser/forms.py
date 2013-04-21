from django import forms

class WallForm(forms.Form):
    wall_content = forms.CharField(widget=forms.Textarea)
