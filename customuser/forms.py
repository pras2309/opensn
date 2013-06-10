from django import forms
from datetime import date
import calendar

years = []
for i in range (1915, date.today().year+1):
    years.append((i, i))
    
months = []
for i in range(1,13):
    months.append((i, calendar.month_name[i]))

days = []
for i in range(1,32):
    days.append((i, i))

class WallForm(forms.Form):
    wall_content = forms.CharField(widget=forms.Textarea)


class SettingsForm(forms.Form):
    enable_email = forms.BooleanField(required=False)
    enable_dob = forms.BooleanField(required=False)
    enable_sex = forms.BooleanField(required=False)

class ProfileEditForm(forms.Form):
    f_name = forms.CharField(max_length=200)
    l_name = forms.CharField(max_length=200)    
    dob_dd = forms.ChoiceField(widget=forms.Select(),  
                             choices = (days),
                              required=False)
    dob_mm = forms.ChoiceField(widget=forms.Select(),  
                             choices = (months),
                              required=False)
    dob_yy = forms.ChoiceField(widget=forms.Select(),  
                             choices = (years),
                             required=False)    
    sex = forms.ChoiceField(widget = forms.RadioSelect(), 
                 choices = ([('M','Male'), ('F','Female'), ]), required = False)
    profile_image = forms.ImageField(required=False)


