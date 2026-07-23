from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, UserLoginForm, EditUserForm
from .models import User, Profile


class UserRegisterView(View):
    form_class = UserRegistrationForm
    templates_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.templates_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                phone_number=cd['phone'],
                full_name=cd['full_name'],
                password=cd['password'],
            )
            Profile.objects.create(user=user)
            messages.success(
                request, "ثبت‌نام شما با موفقیت انجام شد", "success")
            return redirect("accounts:user_login")
        return render(request, self.templates_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    templates_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.templates_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(
                    request, "ورود شما با موفقیت انجام شد", "success")
                return redirect("home:home")
            else:
                form.add_error(None, "شماره تلفن یا رمز عبور اشتباه است")
        return render(request, self.templates_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "شما با موفقیت خارج شدید", "success")
        return redirect("home:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        profile = get_object_or_404(Profile, user=user)
        return render(request, "accounts/profile.html", {"user": user, "profile": profile})


class EditUserView(LoginRequiredMixin, View):
    form_class = EditUserForm

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(
            instance=profile,
            initial={'phone': request.user.phone_number}
        )
        return render(request, "accounts/edit_profile.html", {"form": form})

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        form = self.form_class(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.phone_number = form.cleaned_data["phone"]
            request.user.save()
            messages.success(
                request, "پروفایل شما با موفقیت ویرایش شد", "success")
        return redirect("accounts:user_profile", request.user.id)
