from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.utils.http import is_safe_url
User = get_user_model()

# from contacts.models import Contact

def register(request):
    context = {}
    if request.method == "POST":
        print('POST')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']
        context = {
            "account": {"first_name": first_name,
            "last_name": last_name, "email": email}
        }
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken')
                return render(request, 'register.html', context)
            elif len(password) < 8:
                messages.error(request, 'Password should be more than 8 characters')
                return render(request, 'register.html', context)
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    email=email
                )
                user.save()
                messages.success(request, 'Thanks! You registred and can login')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html', context)

    else:
        return render(request, 'register.html', context)

def login(request):
    context = {}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if request.user.is_authenticated==False:
        if request.method == "POST":
            # Register user
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            context = {
            "account": {"email": email}
            }
            if user is not None:
                auth.login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html', {})
    return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('login')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {})
    return render(request, 'login.html', {})



