def user_preferred_language(request):
    if request.user.is_authenticated:
        return {'preferred_language': request.user.userprofile.preferred_language}
    return {}