from django.urls import path
from . import views

urlpatterns = [
    path('/horizontal', views.learn_flexbox_horizontal, name = "learn_flexbox_horizontal"),
    path('/vertical', views.learn_flexbox_vertical, name = "learn_flexbox_vertical"),
]