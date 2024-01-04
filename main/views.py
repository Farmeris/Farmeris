from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from login_app.models import UserProfile
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


def main(request):

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        filter_trusted = user_profile.filter_trusted
    else:
        user_profile = None
        filter_trusted = True

    #all_products = Polozka.objects.all()
    query = request.GET.get('query')

    if query:
        base_query = Polozka.objects.filter(
            Q(nazov_produktu__icontains=query) |
            Q(user_profile__user__username__icontains=query)
        )
        if filter_trusted:
            # Filter to only show products from trusted users
            all_products = base_query.filter(user_profile__is_trusted=True)
        else:
            all_products = base_query
    else:
        if filter_trusted:
            # Show only products from trusted users
            all_products = Polozka.objects.filter(user_profile__is_trusted=True)
        else:
            # Show all products
            all_products = Polozka.objects.all()
            all_products = all_products.order_by('-created_at')

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
    return render(request, 'main.html', context)
