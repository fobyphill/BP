from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from app.models import Item, Transfer, ItemTransfer, StatusTransfer
from django.urls import reverse
from .. import send_email


def index(request):
    return HttpResponseRedirect(reverse("sales"))

def sales(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(is_active=True)
        ctx = {
            'title': 'Sales',
            'items': items
        }
        return render(request, "sales/index.html", ctx)
    else:
        return HttpResponseRedirect(reverse("login"))

# Создание заказа
def order_view(request):
    if request.method == "POST":
        transfer = Transfer.objects.create(user_id=request.user.id,)  # Создали заказ
        q = 0; t = 0.0; item_id = 0  # временные переменные для количества, стоимости и  айди товара
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                if key[len(key)-5:] == 'total':
                    t = float(request.POST[key])
                else:
                    q = int(request.POST[key])
                    item_id = int(key)
                if t != 0 and q != 0:
                    #Изменим остатки на складе
                    ItemTransfer.objects.create(quantity=q, item_id=item_id,
                                                transfer_id=transfer.id, total=t)  # добавили количество и ид товаров
                    item = Item.objects.get(id=item_id)
                    item.stock = item.stock - q
                    item.save()
                    q = 0; t = 0; item_id = 0
                    # Отправим письма
        #             client_letter_body = "Вы оформили заказ. Номер заказа - {}. В ближайшее время мы Вам перезвоним".format(transfer.id)
        #             manager_letter_body = "Клиент id {0} {2} {3} оформил новый заказ № {1}.".format(request.user.id, transfer.id,
        #                                                                                             request.user.first_name, request.user.last_name)
        #             client_mail = request.user.email
        #             manager_mail = request.user.manager_id
        #             subject = 'Новый заказ №{}'.format(transfer.id)
        #             send_email.SendMail(client_mail, subject, client_letter_body)
        #             send_email.SendMail(manager_mail, subject, manager_letter_body)
        # return render(request, 'order.html', context={'order_id': transfer.id})
    else:
        return HttpResponseRedirect(reverse("index"))

# Переход на страницу заказов
def orders(request):
    orders = Transfer.objects.filter(user_id=request.user.id).annotate(total=Sum('itemtransfer__total'))
    ctx = {
        'title': 'Ваши заказы',
        'orders': orders,
    }
    return render(request, 'sales/orders.html', ctx)
