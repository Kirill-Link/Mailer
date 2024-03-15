from django.urls import path

import main.views
from main import views

urlpatterns = [
    path('', views.index, name="main"),
    path('detail/<int:mail_id>/', views.detail, name="detail"),
]