from django.urls import path
from .views import UserRegisterView, UserRegisterVerifyCodeView, UserLoginView, UserLogoutView

app_name = 'accounts'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('verify/', UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
]