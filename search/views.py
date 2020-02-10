from django.shortcuts import render
from products.models import Product

def search(request):
    context = {}
    query = request.GET.get('q', None)
    if query is not None:
        object_list = Product.objects.search(query)
        context = {
            "object_list": object_list
        }
    return render(request, 'search.html', context)