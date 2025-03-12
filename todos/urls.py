from django.urls import path

# from .views import Todos, TodoDetail
from . import views

urlpatterns = [
    path("", views.Todos.as_view()),
    path("<int:pk>", views.TodoDetail.as_view()),
]
