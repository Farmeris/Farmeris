from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone

def user_stats(request):
    total_users = User.objects.filter(is_superuser=False).count()

    # Get active user sessions (logged-in users)
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    return {
        'total_users': total_users,
    }

def css_styles(request):
    return {
        'global_css_styles': [
            'css/polozka_newx.css',
            'css/root.css',
            'css/root2.css',
            'css/general_mobile_styles.css',
            'css/merged_icons.css',
            'css/footer.css',
            'css/pagination.css',
            'css/2polozka_cena_pridanie.css',
            'css/tabler-icons.css'
        ]
    }