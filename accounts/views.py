from django.shortcuts import render


def login(request):
    context = {
        'login': 'hello'
    }
    return render(request, 'login.html', context)


def register(request):
    context = {
        'register': 'register'
    }
    return render(request, 'register.html', context)