from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    # path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/notification/", views.NotificationListView.as_view(), name="profile-notification"),    
    path('profile/notifications/read/<int:pk>/', views.mark_notification_read, name='mark-notification-read'),

]
