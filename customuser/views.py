# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *
from customuser.forms import WallForm, SettingsForm,  ProfileEditForm
import subprocess
from opensn.settings import SITE_ROOT
import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
import datetime

@login_required
def home(request):
    return render(request, 'registration/home.html', {'user_info':request.user}) 

@login_required
def profile(request, message = None):
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
        'form' : form,
        'message': message
    })


@login_required
@csrf_exempt
def vote(request):
    #FIXME: Vote controller pending
    post_data = request.POST
    wall = Wall.objects.get(pk=post_data["unique_id"])
    json_resp = {}
    if post_data["vote"]=='up':
        wall.vote_up = 1
        wall.vote_down = 0
        json_resp['vote_up'] ='1'
    elif post_data["vote"]=='down':
        wall.vote_up = 0
        wall.vote_down = 1
        json_resp['vote_down'] = 1
    wall.save()
    json_resp = simplejson.dumps(json_resp)
    return HttpResponse(json_resp, mimetype="application/json") 

@login_required
def user_profile(request, user_id):
    
    user_id = int(user_id)
    user_data =  userProfile(user_id)
    
    return render(request, 'registration/profile_user.html', {
        'user_data': user_data[0],
        'user_info':request.user,
    })

@login_required
def profile_edit(request):
    
    user_id = request.user.id
    user_data =  userProfile(user_id)
    user_data = user_data[0]
    dob = user_data["date_of_birth"].split('/');
    user_data['dob_dd'] = int(dob[0])
    user_data['dob_mm'] = int(dob[1])
    user_data['dob_yy'] = int(dob[2])
    
    form = ProfileEditForm(user_data)
    message = ''
    
    if request.method == 'POST': # If the form has been submitted...
        form = ProfileEditForm(request.POST, request.FILES) # A form bound to the POST data
        #import ipdb;ipdb.set_trace()

        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            post_data = form.cleaned_data
            post_data['date_of_birth'] = post_data['dob_mm']+"/"+post_data['dob_dd']+"/"+post_data['dob_yy']
            custom_user = CustomUser.objects.get(user_id=user_id)
            custom_user.f_name=post_data['f_name']
            custom_user.l_name=post_data['l_name']
            custom_user.date_of_birth=post_data['date_of_birth']
            custom_user.sex=post_data['sex'] 
            if post_data['profile_image']:
                custom_user.profile_image = post_data['profile_image']
            custom_user.save()
            message = "Profile updated successfully"
            HttpResponseRedirect('/me')
                
    return render(request, 'registration/user_edit_form.html', {
        'user_data': user_data,
        'user_info':request.user,
        'form': form,
        'message': message
    })

@login_required
def profile_edit_success(request):
    return render(request, 'registration/user_edit_succeess.html')
    

@login_required
def wall(request):
    wall_obj = Wall()
    wall_data = wall_obj.wallContent(user_id=request.user.id)
    
    return render(request, 'registration/wall.html', {
        'user_info':request.user,
        'wall_data': wall_data,
    })

@login_required
def friends(request):
    return render(request, 'customuser/friends.html', {
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
@csrf_exempt
def searchUrls(request):
    post_data = request.POST
    text = str(post_data["text"])
    description = str(post_data["description"])
    url = "php "+SITE_ROOT+ "/utils/searchUrls.php '"+text+"' '"+description+"'"
    proc = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    json_resp = proc.stdout.read()
    parse_json = simplejson.loads(json_resp)
    
    parse_json['videoFlag'] = post_data['videoFlag']
    parse_json['videoIframe'] = post_data['videoIframe']
    parse_json['imageId'] = post_data['imageId']
    parse_json['pTP'] = post_data['pTP']
    parse_json['pDP'] = post_data['pDP']
    parse_json['imgSrc'] = post_data['imgSrc']
    parse_json['contentWidth'] = post_data['contentWidth']
    parse_json['hrefUrl'] = post_data['hrefUrl']
    parse_json['title'] = post_data['title']
    parse_json['fancyUrl'] = post_data['fancyUrl']
    now = datetime.datetime.now()
    date_time = now.strftime('%Y-%m-%d %H:%M:%S')

    parse_json = simplejson.dumps(parse_json)

    rec = Wall(user_id=request.user.id, wall_content=parse_json, date_time = date_time)
    rec.save()
    return HttpResponse(json_resp, mimetype="application/json") 

@login_required
def textCrawler(request):
    text = str(request.GET["text"])
    url = "php "+SITE_ROOT+ "/utils/textCrawler.php "+text
    proc = subprocess.Popen(url, shell=True, stdout=subprocess.PIPE)
    json_resp = proc.stdout.read()

    return HttpResponse(json_resp, mimetype="application/json") 
