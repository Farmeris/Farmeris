
from django.utils.translation import get_language


def user_preferred_language(request):
    if request.user.is_authenticated:
        return {'preferred_language': request.user.userprofile.preferred_language}
    return {}

def current_language(request):
    return {'current_language': get_language()}
