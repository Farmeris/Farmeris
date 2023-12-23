from django.utils import translation
from django.urls import reverse
from django.conf import settings
from .models import UserProfile

class SetUserPreferredLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language_to_set = settings.LANGUAGE_CODE  # Default to the language set in settings

        # If the user is changing their preferred language through the "/set_language/" POST request
        if request.path == reverse('set_language') and request.method == "POST":
            chosen_language = request.POST.get("language")
            if chosen_language:
                language_to_set = chosen_language

                if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
                    user_profile = request.user.userprofile
                    user_profile.preferred_language = chosen_language
                    user_profile.save()

        # If the user is authenticated, set the language to the user's preferred language
        elif request.user.is_authenticated and hasattr(request.user, 'userprofile'):
            preferred_language = request.user.userprofile.preferred_language
            if preferred_language:
                language_to_set = preferred_language

        # Activate the chosen language for this session
        translation.activate(language_to_set)
        request.session['django_language'] = language_to_set
        
        response = self.get_response(request)
        return response

class UpdateFilterTrustedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and 'filter_trusted' in request.POST:
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.filter_trusted = request.POST.get('filter_trusted') == 'True'
                user_profile.save()
                return redirect(request.path)

        response = self.get_response(request)
        return response
