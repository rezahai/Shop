from django.urls import path, include
from .views import HomeView, ProductDetailVew, BucketHomeView, DeleteBuketObjectView, DownloadBucketObjectView

app_name = 'home'

bucket_urls = [
    path('', BucketHomeView.as_view(), name='bucket'),  # It is placed above the rest
    path('delete_obj/<str:key>/', DeleteBuketObjectView.as_view(), name='delete_obj_bucket'),
    path('download_obj_bucket/<str:key>/', DownloadBucketObjectView.as_view(), name='download_obj_bucket'),
]

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('bucket/', include(bucket_urls)),
    path('<slug:slug>/', ProductDetailVew.as_view(), name='product_detail'),
]
