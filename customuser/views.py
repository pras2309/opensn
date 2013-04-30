# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *
from customuser.forms import WallForm, SettingsForm
import subprocess

@login_required
def home(request):
    return render(request, 'registration/home.html', {'user_info':request.user}) 

@login_required
def profile(request):

    user_data =  userProfile(request.user.id)
    wall_obj = Wall()
    wall_data = wall_obj.wallContent(user_id=request.user.id)
    
    form = WallForm()
    if request.method == 'POST': # If the form has been submitted...
        form = WallForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            post_data = request.POST
            rec = Wall(user_id=request.user.id,
                               wall_content=post_data["wall_content"])
            rec.save()
            return HttpResponseRedirect('/me') # Redirect after POST
    
    return render(request, 'registration/profile.html', {
        'user_data': user_data[0],
        'user_info':request.user,
        'wall_data': wall_data,
        'form' : form
    })

@login_required
def user_profile(request, user_id):
    
    user_id = int(user_id)
    user_data =  userProfile(user_id)
    
    return render(request, 'registration/profile_user.html', {
        'user_data': user_data[0],
        'user_info':request.user,
    })
    
@login_required
def wall(request):
    wall_obj = Wall()
    wall_data = wall_obj.wallContent(user_id=request.user.id)
    
    return render(request, 'registration/wall.html', {
        'user_info':request.user,
        'wall_data': wall_data,
    })


@login_required
def settings(request):

    user_id = int(request.user.id)
    user_data =  userProfile(user_id)
    message = ''
    form = SettingsForm()
    if request.method == 'POST': # If the form has been submitted...
        form = SettingsForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
            
            post_data = form.cleaned_data
            updateSettings (user_id, int(post_data["enable_email"]), 
                                         int(post_data["enable_dob"]), int(post_data["enable_sex"]))
            user_data =  userProfile(user_id)
            message = "Settings updated successfully"
    return render(request, 'customuser/settings.html', {
        'user_info':request.user,
        'form': form,
        'user_data':user_data[0],
        'message':message
    })


@login_required
def searchUrls(request):
    text = str(request.GET["text"])
    description = str(request.GET["description"])
    url = "php /Users/prashantagarwal/Projects/phptest/searchUrls.php '"+text+"' '"+description+"'"
    proc = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    json = proc.stdout.read()
    return HttpResponse(json, mimetype="application/json") 

@login_required
def textCrawler(request):
    text = str(request.GET["text"])
    proc = subprocess.Popen("php /Users/prashantagarwal/Projects/phptest/textCrawler.php "+text, shell=True, stdout=subprocess.PIPE)
    json = proc.stdout.read()
    return HttpResponse(json, mimetype="application/json") 
