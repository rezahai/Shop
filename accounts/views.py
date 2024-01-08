from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
from django.contrib.auth import login, logout, authenticate
from .models import OtpCode, User
import random
from utils import send_otp_code
from datetime import  timedelta


class UserRegisterView(View):
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9996)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent your sms', 'success')
            return redirect('accounts:verify_code')
        return render(request, 'accounts/register.html', {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            now = timezone.now()
            expired_time = code_instance.created + timedelta(minutes=1)
            cd = form.cleaned_data
            if cd['code'] == code_instance.code and now < expired_time:
                User.objects.create(phone_number=user_session['phone_number'], email=user_session['email'],
                                    full_name=user_session['full_name'], password=user_session['password'])
                code_instance.delete()
                messages.success(request, 'user registered successfully', 'success')
                return redirect('home:home')
            elif now > expired_time:
                code_instance.delete()
                messages.error(request, 'code expired', 'danger')
                return redirect('accounts:user_register')
            else:
                messages.error(request, 'the code is not valid', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you are logged in', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'password or phone number is not valid', 'danger')
        return render(request, 'accounts/login.html', {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, 'you are logged out', 'success')
            return redirect('home:home')

