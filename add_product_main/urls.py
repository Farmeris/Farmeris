from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from add_product_main import views as add_product_views


app_name = 'add_product_main'

urlpatterns = [
    path('<str:username>/polozka/pridanie/', add_product_views.pridaj_polozku, name='user_pridaj_polozku'),
    path('<str:username>/doprava/pridanie/delete/<int:transport_id>/', add_product_views.delete_transport, name='user_delete_transport'),
    path('<str:username>/transportloc/<int:transportloc_id>/delete/', add_product_views.delete_transport_loc, name='delete_transport_loc'),
    path('<str:username>/doprava/<str:nazov_produktu>/select/<int:transport_id>/', add_product_views.select_transport, name='user_select_transport'),
    path('<str:username>/doprava/<str:nazov_produktu>/deselect/<int:transport_id>/', add_product_views.deselect_transport, name='user_deselect_transport'),
    path('<str:username>/doprava/pridanie/', add_product_views.pridaj_dopravu, name='user_pridaj_dopravu'),
    path('<str:username>/polozka/<str:nazov_produktu>/', add_product_views.zobraz_polozku, name='user_zobraz_polozku'),
    path('<str:username>/polozka/<str:nazov_produktu>/<int:anchor>/', add_product_views.zobraz_polozku, name='user_zobraz_polozku'),
    path('<str:username>/polozka/<str:nazov_produktu>/delete/<int:cena_id>/', add_product_views.delete_cena, name='user_delete_cena'),
    path('<str:username>/delete_picture/<int:product_id>/', add_product_views.delete_picture, name='delete_picture'),
    path('<str:username>/polozka/<str:nazov_produktu>/add_picture/', add_product_views.add_picture, name='add_picture'),
] 

# Add the following line to handle media files
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
