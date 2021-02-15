import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from app.models import UserAccount, Item, UserPainInformation


def index(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(is_active=True)
        ctx = {
            'title': 'Sales',
            'items': items
        }
        return render(request, "sales/index.html", ctx)
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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        inn = request.POST["inn"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        if firstname == '' or lastname == '' or inn == '':
            return render(request, 'register.html', {
                'message': "Заполните пожалуйста все поля."
            })

        # Attempt to create new user
        try:
            UserAccount.objects.create_user(email, email, password,
                                            first_name=firstname, last_name=lastname, is_active=False,)

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Token 99afce8b29b74ee40ef10c17644c2e6be81dec49',
                'X-Secret': 'fb51656eb2305e92633b6fdd8309059255602dee'
            }

            data = '{ "query": "0123456789" }'
            response = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party',
                                     headers=headers, data=data)
            load_info = json.loads(response.text)
            user_login = authenticate(request, username=email, password=password)

            UserPainInformation.objects.create(id_id=1)
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Email address or INN already taken."
                })
        return render(request, "login.html", {
            "message": "ждите модерации"
        })
    else:
        return render(request, "register.html")