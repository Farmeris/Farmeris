from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from login_app.models import UserProfile

def main(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = get_object_or_404(User, username=username)
        user_profile = get_object_or_404(UserProfile, user__username=username)

        context = {
            'username': username,
            'user_profile': user_profile,
        }
    else:
        # Handle the case when the user is not logged in
        context = {}

    return render(request, 'main.html', context)