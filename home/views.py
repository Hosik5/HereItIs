from django.shortcuts import render
from .models import Search_history
from .models import Member_info

# HOME
def home(request):
    return render(request, 'home.html')

# FAQ
def faq(request):
    return render(request, 'faq.html')

# SEARCH
def search(request):
    searchbox = request.GET.get('searchbox')
    context = {
        'searchbox' : searchbox,
    }
    return render(request, 'search.html', context)
