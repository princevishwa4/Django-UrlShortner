from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
from .models import shortUrl
import random, string


def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login') 
    else:
        user = request.user
        urls = shortUrl.objects.filter(user=user)        
        return  render(request, 'authentication/dashboard.html', {'urls': urls})


def randomgen():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(8))


def generate(request):
    if request.method == "POST":
        if request.POST['original'] and request.POST['short']:
            user = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shortUrl.objects.filter(short_query=short)
            if not check:
                newurl = shortUrl(
                    user = user,
                    original_url = original,
                    short_query = short
                )
                newurl.save()
                return HttpResponseRedirect('/dashboard')
            else:
                messages.error(request, "Short Name Already Exist.")
                return HttpResponseRedirect('/dashboard')
        elif request.POST['original']:
            user = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shortUrl.objects.filter(short_query=short)
                if not check:
                    newurl = shortUrl(
                        user = user,
                        original_url = original,
                        short_query = short
                    )
                    newurl.save()
                    return HttpResponseRedirect('/dashboard')
                else:
                    continue
        else:
            messages.error(request, "Empty Fields.")
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')


def redirectUrl(request, query):
    if not query or query is None:
        return HttpResponseRedirect('/dashboard')
    else:
        try:
            check = shortUrl.objects.get(short_query=query)
            check.visits = check.visits + 1
            check.save()
            originalRedirectionUrl = check.original_url
            return HttpResponseRedirect(originalRedirectionUrl) 
        except Exception:
            return render(request, 'authentication/error.html')


def deleteurl(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            short = request.POST['delete']
            try:
                check = shortUrl.objects.filter(short_query=short)
                check.delete()
                return HttpResponseRedirect('/dashboard')
            except shorturl.DoesNotExist:
                return render(request, 'authentication/error.html')
        else:
            return render(request, 'authentication/error.html')
    else:
        return HttpResponseRedirect('/login')
