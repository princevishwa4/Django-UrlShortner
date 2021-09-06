from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['email'] and request.POST['password']:
                try:
                    user = User.objects.get(email=request.POST['email'])
                    login(request, user)
                    return HttpResponseRedirect('/dashboard')
                except User.DoesNotExist:
                    return render(request, 'authentication/login.html', {"error" : "User Does Not Exist"}) 
            else:
                return render(request, 'authentication/login.html', {"error" : "Fields Are Empty"})  
        else:
            return render(request, 'authentication/login.html')
    else:
        return HttpResponseRedirect('/dashboard')

def register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            if request.POST['password'] == request.POST['password2']:
                if request.POST['username'] and request.POST['email'] and request.POST['password']:
                    try:
                        user = User.objects.get(email=request.POST['email'])
                    except User.DoesNotExist:
                        User.objects.create_user(
                            username=request.POST['username'], 
                            email=request.POST['email'], 
                            password=request.POST['password']
                            )
                        messages.success(request, "Registered Successfully.")
                        return HttpResponseRedirect('/login')
                else:
                    return render(request, 'authentication/register.html', {"error" : "Fields Are Empty"}) 
            else:
                return render(request, 'authentication/register.html', {"error" : "Password Don't Match"})
        else:
            return render(request, 'authentication/register.html')
    else:
        return HttpResponseRedirect('/dashboard')

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html') 
    else:
        return render(request, 'authentication/dashboard.html') 


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')               
