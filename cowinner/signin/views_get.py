from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def signin(request):
    return render(request, 'pages/signin.html')