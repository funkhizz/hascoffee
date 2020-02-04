from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    context = {'object_list': '1234',
    'new_object_list': '12345'}
    return render(request, 'homepage.html', context)

