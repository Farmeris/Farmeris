from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from login_app.models import UserProfile
from django.contrib.auth.models import User
from add_product_main.models import Polozka
from datetime import datetime
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import QueryDict

import pytz

def search(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    else:
        user_profile = None
    #all_products = Polozka.objects.all()
    query = request.GET.get('query')

    if query:
        # Filter the records based on the query
        all_products = Polozka.objects.filter(
            Q(nazov_produktu__icontains=query) | 
            Q(user_profile__user__username__icontains=query)
        ).order_by('-created_at')
    else:
        all_products = Polozka.objects.all().order_by('-created_at')

    
    #pagination
    if request.user.is_authenticated:
        default_pagination = user_profile.pagination_preference
    else:
        default_pagination = 10  # or any default value you want for non-logged in users
        
    items_per_page = int(request.GET.get('items_per_page', default_pagination)) 

    paginator = Paginator(all_products, items_per_page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    #saved pagination for user
    if request.user.is_authenticated and items_per_page != default_pagination:
        user_profile.pagination_preference = items_per_page
        user_profile.save()
    #end of pagination

    # Preserve the query parameter in the pagination links
    query_params = QueryDict(mutable=True)
    if query:
        query_params['query'] = query
    
    context = {
        'products': products,
        'user_profile': user_profile,
        'items_per_page': items_per_page,
        'query_params': query_params.urlencode(),
    }
    return render(request, 'search.html', context)

def search2(request):
    user_profile = UserProfile.objects.get(user=request.user)
    #all_products = Polozka.objects.all()
    query = request.GET.get('query')

    if query:
        # Filter the records based on the query
        all_products = Polozka.objects.filter(Q(nazov_produktu__icontains=query))
    else:
        all_products = Polozka.objects.all()
    
    context = {
        'user_profile': user_profile,
        'products': all_products,
    }
    return render(request, 'search2.html', context)