from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_profile import views


app_name = 'user_profile'

urlpatterns = [
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('<str:username>/edit/', views.user_profile_edit, name='user_profile_edit'),
    path('<str:username>/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
] 