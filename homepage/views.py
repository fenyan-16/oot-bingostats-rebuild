from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'homepage/index_d.html', {})

def index2(request):
    return render(request, 'homepage/index.html', {})

def bingo(request):
    return render(request, '')