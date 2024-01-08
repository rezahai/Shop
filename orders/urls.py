from django.urls import path
from .views import CartView, CarrAddView


app_name = 'orders'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart_add/<int:product_id>/', CarrAddView.as_view(), name='cart_add'),
]