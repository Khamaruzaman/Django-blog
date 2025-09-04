from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView

from .forms import ProfileUpdateForm, UserLoginForm, UserRegisterForm, UserUpdateForm
from .models import Notification


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}. Login to continue"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    context = {"title": "Register", "form": form}

    return render(request, "users/register.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile Updated!")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.FILES, instance=request.user.profile)

    context = {
        "title": f"{request.user.username}'s profile",
        "u_form": u_form,
        "p_form": p_form,
    }
    return render(request, "users/profile.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")
            else:
                messages.warning(request, "Invalid username or password.")
                return redirect("profile")
        else:
            return render(request, "users/login.html", {"form": form})
    else:
        form = UserLoginForm()
    context = {"title": "Login", "form": form}
    return render(request, "users/login.html", context)


class NotificationListView(ListView):
    model = Notification
    template_name = "users/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return (
            Notification.objects.filter(user=self.request.user)
            .order_by("-created_at")
            .values("pk","message", "created_at", "is_read")
        )


def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('profile-notification')  
