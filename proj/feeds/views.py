from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def feeds(request):
    context = {}
    return render(request, 'feeds/feeds.html', context)