from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from app.models import Item, Transfer, ItemTransfer, StatusTransfer
from django.urls import reverse


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

def order_view(request):
    if request.method == "POST":
        transfer = Transfer.objects.create(user_id=request.user.id,)  # Создали заказ
        q = ''; t = ''; item_id = ''  # временные переменные для количества, стоимости и  айди товара
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                if key[len(key)-5:] == 'total':
                    t = request.POST[key]
                else:
                    q = request.POST[key]
                    item_id = key
                if t != '' and q != '':
                    ItemTransfer.objects.create(quantity=q, item_id=item_id,
                                                transfer_id=transfer.id, total=t)  # добавили количество и ид товаров
                    q = ''; t = ''; item_id = ''
        return render(request, 'order.html', context={'order_id': transfer.id})
    else:
        return HttpResponseRedirect(reverse("index"))

def orders(request):
    orders = Transfer.objects.filter(user_id=request.user.id).annotate(total=Sum('itemtransfer__total'))
    ctx = {
        'title': 'Ваши заказы',
        'orders': orders,
    }
    return render(request, 'sales/orders.html', ctx)
