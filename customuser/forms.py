from django import forms

class WallForm(forms.Form):
    wall_content = forms.CharField(widget=forms.Textarea)


class SettingsForm(forms.Form):
    enable_email = forms.BooleanField(required=False)
    enable_dob = forms.BooleanField(required=False)
    enable_sex = forms.BooleanField(required=False)
