# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *


def aboutus(request):
    return render(request, 'general/aboutus.html', {'user_info':request.user}) 

def terms(request):
    return render(request, 'general/terms.html', {'user_info':request.user})

def privacy(request):
    return render(request, 'general/privacy.html', {'user_info':request.user})

def blog(request):
    return render(request, 'general/blog.html', {'user_info':request.user})
