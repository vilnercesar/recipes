from django.http import HttpResponse
from django.shortcuts import render

# from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'recipes/home.html', context={
        'nome': 'Vilner César'
    })


def sobre(request):
    return render(request, 'me-apague/temp.html')


def contato(request):
    return HttpResponse('CONTATO')
