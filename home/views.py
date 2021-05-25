from django.shortcuts import render
from home.models import Search_history

# Create your views here.

def home(request):
    return render(request, 'home.html')

def faq(request):
    return render(request, 'faq.html')