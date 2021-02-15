from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from app.models import Item, Transfer, ItemTransfer
from django.urls import reverse


def index(request):
    items = Item.objects.filter(is_active=True)
    ctx = {
        'title': 'Sales',
        'items': items
    }
    return render(request, 'sales/index.html', ctx)

def order_view(request):
    if request.method == "POST":
        transfer = Transfer.objects.create(user_id=request.user.id)  # Создали заказ
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                ItemTransfer.objects.create(quantity=request.POST[key], item_id=key,
                                            transfer_id=transfer.id)  # добавили количество и ид товаров
        return render(request, 'order.html', context={'order_id': transfer.id})
    else:
        return HttpResponseRedirect(reverse("index"))
