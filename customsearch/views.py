# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customuser.models import *

@login_required
def home(request, q=None):
    search_string = request.GET.get('q')
    
    if search_string:
        search_results = searchQuery(search_string)
    else:
        search_results = None
    return render(request, 'customsearch/home.html',{
                 'user_info':request.user,
                 'q':search_string,
                 'search_results':search_results,
                 'result_count': len(search_results)
                })  