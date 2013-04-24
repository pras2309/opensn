# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *
from customuser.forms import WallForm

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