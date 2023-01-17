from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'inventory/home.html')

def index(request):
    return render(request, 'inventory/index.html')

def about(request):
    return render(request, 'inventory/about.html')

def contact(request):
    return render(request, 'inventory/contact.html')




