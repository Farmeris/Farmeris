def avatar_processor(request):
    if not request.user.is_authenticated:
        return {'avatar_url': None}

    user_profile = getattr(request.user, 'userprofile', None)
    
    if user_profile and user_profile.avatar and hasattr(user_profile.avatar, 'url'):
        return {'avatar_url': user_profile.avatar.url}

    # Check for Google avatar
    try:
        google_account = request.user.socialaccount_set.filter(provider='google').first()
        if google_account:
            google_avatar_url = google_account.extra_data.get('picture')
            if google_avatar_url:
                return {'avatar_url': google_avatar_url}
    except (AttributeError, ValueError):
        pass

    return {'avatar_url': None}