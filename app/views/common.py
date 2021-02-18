import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from app.models import UserAccount, Item, UserPainInformation
from .. import send_email


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
            return HttpResponseRedirect(reverse("sales"))
        else:
            return render(request, "login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("sales"))

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
            #Загружаем данные пользователя с Дадаты
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Token 99afce8b29b74ee40ef10c17644c2e6be81dec49',
                'X-Secret': 'fb51656eb2305e92633b6fdd8309059255602dee'
            }
            # 1840010623 - IP
            # 6168105283 - Legal F-trade
            # 665800657455 - titov IP
            # 7825098536 - Kvantum Legal
            data = '{ "query": "'+inn+'" }'
            response = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party',
                                     headers=headers, data=data)
            load_info = json.loads(response.text)
            #Закончили загрузку с дадаты

            if load_info['suggestions']:# если дадата вернула результат, т.е. ИНН существует
                if UserPainInformation.objects.filter(inn=inn).count() == 0:# Если в системе еще нет пользователя с таким ИНН
                    user_account = UserAccount.objects.create_user(email, email, password,
                                                                   first_name=firstname, last_name=lastname,
                                                                   is_active=True, )
                    if load_info['suggestions'][0]['data']['type'] == 'INDIVIDUAL':#Для ИП
                        UserPainInformation.objects.create(id_id=user_account.id,
                                                           inn=load_info['suggestions'][0]['data']['inn'],
                                                           ogrn=load_info['suggestions'][0]['data']['ogrn'],
                                                           okpo=load_info['suggestions'][0]['data']['okpo'],
                                                           oktmo=load_info['suggestions'][0]['data']['oktmo'],
                                                           legal_address=load_info['suggestions'][0]['data']['address'][
                                                               'unrestricted_value'],
                                                           full_name=load_info['suggestions'][0]['value'],
                                                           state_status=load_info['suggestions'][0]['data']['state'][
                                                               'status'],
                                                           type=load_info['suggestions'][0]['data']['type'])
                    else:#Для предприятий
                        UserPainInformation.objects.create(id_id=user_account.id, inn=load_info['suggestions'][0]['data']['inn'],
                                                           kpp=load_info['suggestions'][0]['data']['kpp'],
                                                           ogrn=load_info['suggestions'][0]['data']['ogrn'],
                                                           okpo=load_info['suggestions'][0]['data']['okpo'],
                                                           oktmo=load_info['suggestions'][0]['data']['oktmo'],
                                                           legal_address=load_info['suggestions'][0]['data']['address']['value'],
                                                           full_name=load_info['suggestions'][0]['data']['name']['full_with_opf'],
                                                           state_status=load_info['suggestions'][0]['data']['state']['status'],
                                                           director=load_info['suggestions'][0]['data']['management']['name'],
                                                           type=load_info['suggestions'][0]['data']['type'])

                    user_account.is_active = False
                    user_account.save()

                    # Извещаем администратора
                    # email_admin = 'www.phill.999@gmail.com' #почта администратора
                    # subject = 'Новый пользователь. ID =' + str(user_account.id) +' '+ user_account.first_name + ' '+ user_account.last_name
                    # body_letter = 'В системе зерегистрировался новый пользователь\n. ' \
                    #               'ID =' + str(user_account.id) +' '+ user_account.first_name + ' '+ user_account.last_name+'\n' \
                    #                 'Проверьте пожалуйста данные и активируйте пользователя.'
                    # send_email.SendMail(email_admin, subject, body_letter)
                    #Конец отправки письма администратору
                else:
                    return render(request, "register.html", {
                        "message": "Введенный ИНН уже зарегистрирован в системе."
                    })
            else:
                return render(request, "register.html", {
                    "message": "Вы ввели некорректный ИНН. Допускаются ИНН ИП или юридического лица"
                })
        except IntegrityError as e:
            print(e)
            return render(request, "register.html", {
                "message": "Email уже зерегистрирована в системе или некорректна."
                })
        return render(request, "login.html", {
            "message": "Успешная регистрация. Пожалуйста подождите. В ближайшее время с Вами свяжется менеджер. "
                       "Аккаунт будет доступен после прохождения процедуры модерации"
        })
    else:
        return render(request, "register.html")