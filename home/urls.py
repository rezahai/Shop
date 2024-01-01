from django.urls import path
from .views import HomeView, ProductDetailVew, BucketHomeView, DeleteBuketObjectView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bucket/', BucketHomeView.as_view(), name='bucket'),  # It is placed above the rest
    path('delete_obj_bucket/<key>', DeleteBuketObjectView.as_view(), name='delete_obj_bucket'),
    path('<slug:slug>/', ProductDetailVew.as_view(), name='product_detail'),
]
