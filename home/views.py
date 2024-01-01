from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Product
from . import tasks


class HomeView(View):
    def get(self, request):
        products = Product.objects.filter(available=True)
        return render(request, 'home/home.html', {'products': products})


class ProductDetailVew(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'home/detail.html', {'product': product})


class BucketHomeView(View):

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, 'home/bucket.html', {'objects': objects})


class DeleteBuketObjectView(View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'you have successfully deleted your object', 'info')
        return redirect('home:bucket')
