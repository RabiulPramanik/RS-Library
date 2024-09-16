from django.shortcuts import render
from django.views.generic import TemplateView
from books.models import BookModel, CategoryModel

def home(request, category_slug=None):
    books = BookModel.objects.all()
    category = CategoryModel.objects.all()
    if category_slug is not None:
        bd = CategoryModel.objects.get(slug = category_slug)
        books = BookModel.objects.filter(category = bd)
    return render(request, "index.html", {"books":books, 'category':category})

class Home(TemplateView):
    template_name = "index.html"

