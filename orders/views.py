from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from home.models import Product
from .cart import Cart
from .forms import CartAddForm

class CartView(View):
    def get(self, request):
        return render(request, 'orders/cart.html')


class CarrAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')
