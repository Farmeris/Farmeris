from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ProductAdd
from datetime import datetime
from .forms import ProductAddForm
import pytz

# Create your views here.

def polozka(request):
    username = request.user.username
    timezone = pytz.timezone('Europe/Bratislava')
    now = datetime.now().strftime("%d. %m. %H:%M:%S")
    context = {'username': username, 'now': now}
    return render(request, 'polozka.html', context)

@login_required
def pridaj_polozku(request):
    username = request.user.username
    timezone = pytz.timezone('Europe/Bratislava')
    now = datetime.now().strftime("%d. %m. %H:%M:%S")
    #context = {'username': username, 'now': now}
    context = {'username': request.user.username, 'now': datetime.now().strftime("%d. %m. %H:%M:%S")}

    if request.method == 'POST':
        form = ProductAddForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['price']:
                form.save()
                return redirect('success-url')
            else:
                form.add_error('price', 'Please enter a price.')
        #return render(request, 'zoznam_poloziek.html', context)
    else:
        form = ProductAddForm()
    
    context['form'] = form
    return render(request, 'pridaj_polozku.html', context)

'''
    if request.method == 'POST':
        nazov_produktu = request.POST['nazov_produktu']
        info_nazov_produktu = request.POST['info_nazov_produktu']
        info_produktu = request.POST['info_produktu']
        amount = request.POST.get('amount')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        currency = request.POST.get('currency')
        #transport = request.POST.get('transport')
        #transport_price = request.POST.get('transport_price')
        #transport_unit = request.POST.get('transport_unit')
        #additional_info = request.POST.get('additional_info')


        ProductAdd.objects.create(
            user=request.user,
            name=nazov_produktu,
            info_title=info_nazov_produktu,
            info=info_produktu,
            amount=amount,
            unit=unit,
            price=price,
            currency=currency
            #transport=transport,
            #transport_price=transport_price,
            #transport_unit=transport_unit,
            #additional_info=additional_info
        )
        # Additional logic for saving other form fields or redirecting
        
        return render(request, 'zoznam_poloziek.html', context)
    return render(request, 'pridaj_polozku.html', context)
'''
@login_required
def zoznam_poloziek(request):
    username = request.user.username
    timezone = pytz.timezone('Europe/Bratislava')
    now = datetime.now().strftime("%d. %m. %H:%M:%S")
    context = {'username': username, 'now': now}


    return render(request, 'zoznam_poloziek.html', context)

def pridaj_dopravu(request):
    username = request.user.username
    timezone = pytz.timezone('Europe/Bratislava')
    now = datetime.now().strftime("%d. %m. %H:%M:%S")
    context = {'username': username, 'now': now}
    return render(request, 'pridaj_dopravu.html', context)


def user_profile(request, username):
    user = User.objects.get(username=username)
#    profile = UserProfile.objects.get(user=user)
    context = {
        'username': username,
        'profile': profile,
#        # Other context variables for the user profile
    }
    return render(request, 'zoznam_poloziek.html', context)