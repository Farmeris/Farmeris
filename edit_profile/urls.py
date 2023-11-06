from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from edit_profile import views as edit_profile_views


app_name = 'edit_profile'

urlpatterns = [
    path('<str:username>/settings/edit', edit_profile_views.profile_editing, name='user_profile_editing'),
] 