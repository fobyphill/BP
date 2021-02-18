from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from app.views import common, sales

urlpatterns = [
    path('', sales.index, name="index"),
    path('sales', sales.sales, name="sales"),
    path("login", common.login_view, name="login"),
    path("logout", common.logout_view, name="logout"),
    path("register", common.register, name="register"),
    path('order', sales.order_view, name="order"),
    path('orders', sales.orders, name="orders"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)