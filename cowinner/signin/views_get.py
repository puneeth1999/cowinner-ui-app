from cowinner.settings import BASE_DIR, MEDIA_ROOT
from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.

def signin(request):
    return render(request, 'pages/signin.html')

def download(request):
    if request.method == "GET":
        my_file_url = os.path.join(MEDIA_ROOT, 'certificates','certificate.pdf')
        context = {
            'my_file_url' : my_file_url
        }
        return render(request, 'pages/download.html', context)
    
def notify(request):
    return render(request, 'pages/notify.html')