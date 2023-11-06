from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from search import views as search_views


app_name = 'search'

urlpatterns = [
    path('search/', search_views.search, name='user_search'),
    path('search2/', search_views.search2, name='user_search2'),
] 