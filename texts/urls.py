
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from texts import views



app_name = 'texts'

urlpatterns = [
    path('raw_milk_manifesto/', views.manifesto, name='manifesto'),
]
