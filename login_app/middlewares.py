from django.http import JsonResponse

def theme_switch_middleware(get_response):

    def middleware(request):
        if request.method == "POST" and "theme" in request.POST:
            theme_changed = False
            if request.user.is_authenticated:
                user_theme = request.user.userprofile.theme
                new_theme = 'dark' if user_theme == 'light' else 'light'
                request.user.userprofile.theme = new_theme
                request.user.userprofile.save()
                theme_changed = True
            else:
                theme = request.POST.get("theme", "light")
                request.session['theme'] = theme
                theme_changed = True
                
            # If it's an AJAX request, return JSON instead of a full page reload
            if theme_changed and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'theme': request.user.userprofile.theme if request.user.is_authenticated else request.session.get('theme')})

        response = get_response(request)
        return response

    return middleware
