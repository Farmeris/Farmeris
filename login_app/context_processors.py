def theme_context(request):
    theme = 'light'
    if request.user.is_authenticated:
        theme = request.user.userprofile.theme
    elif 'theme' in request.session:
        theme = request.session['theme']
    return {'theme': theme}