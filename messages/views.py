# Create your views here.
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *


def home(request):
    return render(request, 'messages/home.html', {'user_info':request.user}) 

