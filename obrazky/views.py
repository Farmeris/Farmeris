from django.shortcuts import render
from add_product_main.models import Polozka
from login_app.models import UserProfile 

def obrazky(request, username, nazov_produktu, filename):
    user_profile = UserProfile.objects.get(user__username=username)
    polozka = Polozka.objects.filter(user_profile=user_profile, nazov_produktu=nazov_produktu).first()    #additional_image = polozka.additional_images.filter(id=image).first()
    
    if polozka and polozka.image:
        image_url = polozka.image.url
    else:
        image_url = None
    #if additional_image:
    #    image_url = polozka.image
    #image_url = polozka.image.url

    context = {
        'username': username,
        'nazov_produktu': nazov_produktu,
        'image_url': image_url,
        'filename': filename,
    }
    return render(request, 'obrazky.html', context)