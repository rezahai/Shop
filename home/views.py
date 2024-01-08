from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from utils import IsAdminUserMixin
from .models import Product, Category
from . import tasks
from orders.forms import CartAddForm


class HomeView(View):
    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailVew(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm
        return render(request, 'home/detail.html', {'product': product, 'form':form})


class BucketHomeView(IsAdminUserMixin, View):

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, 'home/bucket.html', {'objects': objects})


class DeleteBuketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'you have successfully deleted your object', 'info')
        return redirect('home:bucket')


class DownloadBucketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object has been downloaded', 'info')
        return redirect('home:bucket')
