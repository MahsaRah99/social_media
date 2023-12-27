from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, Relation
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm, EditProfileForm
from .verification import OtpCode
from utils import send_otp_code
import random


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "users/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("posts:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(10000, 99999)
            send_otp_code(form.cleaned_data["email"], random_code)
            OtpCode.objects.create(email=form.cleaned_data["email"], code=random_code)
            request.session["user_registration_info"] = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "we sent you a code", "success")
            return redirect("users:verify_code")
        return render(request, self.template_name, {"form": form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "users/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(email=user_session["email"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_instance.code:
                User.objects.create_user(
                    user_session["username"],
                    user_session["email"],
                    user_session["password"],
                )

                code_instance.delete()
                messages.success(request, "you registered.", "success")
                return redirect("posts:home")
            else:
                messages.error(request, "this code is wrong", "danger")
                return redirect("users:verify_code")
        return redirect("posts:home")


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "users/login.html"

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("posts:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd["email"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "you logged in successfully", "info")
                if self.next:
                    return redirect(self.next)
                return redirect("posts:home")
            messages.error(request, "email or password is wrong", "warning")
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", "success")
        return redirect("posts:home")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all(is_active=True)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        return render(
            request,
            "users/profile.html",
            {"user": user, "posts": posts, "is_following": is_following},
        )


class EditUserProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, "users/edit_profile.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "profile edited successfully", "success")
        return redirect("users:user_profile", request.user.id)


class UserFollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        if user.id != request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "you cant follow/unfollow your account", "danger")
            return redirect("users:user_profile", user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "you are already following this user", "danger")
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, "you followed this user", "success")
        return redirect("users:user_profile", user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs["user_id"])
        if user.id != request.user.id:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(request, "you cant follow/unfollow your account", "danger")
            return redirect("users:user_profile", user.id)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "you unfollowed this user", "success")
        else:
            messages.error(request, "you are not following this user", "danger")
        return redirect("users:user_profile", user.id)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/password_reset_form.html"
    success_url = reverse_lazy("users:password_reset_done")
    email_template_name = "users/password_reset_email.html"


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = reverse_lazy("users:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
