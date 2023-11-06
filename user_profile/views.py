from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse
from login_app.models import UserProfile  # Update the import statement
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from user_profile.forms import UserProfileForm
from add_product_main.models import Polozka, Cena, Transport
from datetime import datetime
from add_product_main.models import PolozkaTransport
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict
import pytz

def user_profile(request, username):

    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user__username=username)
    transport_list = Transport.objects.filter(user_profile=user_profile)
    products = Polozka.objects.filter(user_profile__user__username=username).order_by('-created_at')
    # For anonymous users (not logged in), set polozka_transport_list to an empty list
    polozka_transport_list = []
    polozka_transport_dict = {}
    
    if request.user.is_authenticated:
        polozka_transport_list = PolozkaTransport.objects.filter(polozka__in=products, transport__user_profile__user=request.user)
        # Create a dictionary with polozka as key and polozka_transport as value
        polozka_transport_dict = {polozka_transport.polozka: polozka_transport for polozka_transport in polozka_transport_list}
        
    # Prefetch the related cena objects for each product to avoid additional queries
    products = products.prefetch_related(
        Prefetch('ceny', queryset=Cena.objects.filter(user_profile=user_profile), to_attr='ceny_list'),
        Prefetch('polozkatransport_set', queryset=PolozkaTransport.objects.select_related('transport').filter(polozka__user_profile=user_profile), to_attr='transport_list')
    )
    
    #search
    query = request.GET.get('query')
    if query:
        products = products.filter(nazov_produktu__icontains=query)
    #search
    #pagination
    if request.user.is_authenticated:
        default_pagination = user_profile.pagination_preference
    else:
        default_pagination = 10  # or any default value you want for non-logged in users
        
    items_per_page = int(request.GET.get('items_per_page', default_pagination))

    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params.pop('page', None)
    #saved pagination for user
    if request.user.is_authenticated and items_per_page != default_pagination:
        user_profile.pagination_preference = items_per_page
        user_profile.save()
    #end of pagination

    #profile = get_object_or_404(UserProfile, user=user)
    context = {
        'username': username,
        'user_profile': user_profile,
        'products': products,
        'items_per_page': items_per_page,
        'polozka_transport_dict': polozka_transport_dict,
        'query_params': query_params.urlencode(),
        'transport_list': transport_list,
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url='user_profile:user_profile')
def user_profile_edit(request, username):
    if request.user.username != username:
        # Redirect or handle unauthorized access
        return HttpResponseForbidden()
        
    user = get_object_or_404(User, username=username)
    user_profile = UserProfile.objects.get(user__username=username)
    products = Polozka.objects.filter(user_profile__user__username=username)
    polozka_transport_list = []
    polozka_transport_dict = {}

    #pagination
    if request.user.is_authenticated:
        default_pagination = user_profile.pagination_preference
    else:
        default_pagination = 10  # or any default value you want for non-logged in users
        
    items_per_page = int(request.GET.get('items_per_page', default_pagination)) - 1 

    paginator = Paginator(products, items_per_page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    query_params = request.GET.copy()
    query_params.pop('page', None)
    #saved pagination for user
    if request.user.is_authenticated and items_per_page + 1 != default_pagination:
        user_profile.pagination_preference = items_per_page + 1
        user_profile.save()
    #end of pagination
    
    #profile = get_object_or_404(UserProfile, user=user)
    context = {
        'username': username,
        'user_profile': user_profile,
        'products': products,
        'items_per_page': items_per_page + 1,
        #'profile': profile,
    }
    return render(request, 'user_profile_edit.html', context)

@login_required(login_url='user_profile:user_profile')
def delete_product(request, username, product_id):
    # Ensure that the user is the owner of the product
    if request.user.username != username:
        return HttpResponseForbidden()

    # Retrieve the product and check if it belongs to the user
    product = get_object_or_404(Polozka, id=product_id, user_profile__user__username=username)

    # Perform the actual deletion
    product.delete()

    # Redirect back to the user profile page
    #return redirect('user_profile:user_profile', username=username)
    # Get the 'next' URL from the query parameters
    next_url = request.GET.get('next', 'user_profile:user_profile')  # Redirect to user profile by default if 'next' is not provided

    # Redirect back to the appropriate URL
    return redirect(next_url, username=username)