from django.urls import path

# from .views import Me
from . import views

urlpatterns = [
    path("me/", views.Me.as_view()),
    path("signup/", views.Signup.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
    path("changepassword/", views.ChangePassword.as_view()),
]
