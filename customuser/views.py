# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *

@login_required
def home(request):
    return render(request, 'registration/home.html', {'user_info':request.user}) 

@login_required
def profile(request):
    user_data =  userProfile(request.user.id)
    return render(request, 'registration/profile.html', {
        'user_data': user_data[0],
        'user_info':request.user        
    })
    
@login_required
def wall(request):
    return render(request, 'wall/index.html', {'user_info':request.user}) 
    