
from django.http import Http404
from django.shortcuts import render

from .models import Recipe

# from utils.recipes.factory import make_recipe


# from django.shortcuts import render


# Create your views here.
def home(request):

    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes
    })


def category(request, category_id):

    recipes = Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id')
    if not recipes:
        raise Http404('Not Found 🙁')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'category': f'{recipes.first().category.name}'
    })


def recipe(request, id):
    recipe = Recipe.objects.filter(id=id)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
