from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    if request.user.is_authenticated:
        ctx = {
            'title': 'Home'
        }
        return render(request, "index.html", ctx)
    else:
        return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        UserAccount = authenticate(request, username=email, password=password)
        # Check if authentication successful
        if UserAccount is not None:
            login(request, UserAccount)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "login.html")