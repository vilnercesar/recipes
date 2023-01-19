
from django.shortcuts import render

# from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'nome': 'Vilner César'
    })
