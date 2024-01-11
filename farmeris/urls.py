from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import path, re_path
from login_app.views import CustomConfirmEmailView
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from email_verification.decorators import email_verification_required
from allauth.account.views import email as allauth_email_view
from allauth.account.views import EmailView
from django.utils.decorators import method_decorator
from email_verification.views import CustomEmailView
from login_app import views as login_views
from django.contrib.auth.decorators import login_required

@method_decorator(email_verification_required, name='dispatch')
class ProtectedEmailView(EmailView):
    pass

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('set_language/', set_language, name='set_language'),
    path('handle_unverified_email/', login_views.handle_unverified_email, name='handle_unverified_email'),
    re_path(r'^account/confirm-email/(?P<key>[-:\w]+)/$', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    path('accounts/resend-confirmation/', login_views.resend_confirmation_email, name='resend_confirmation_email'),
    # path('accounts/email/', email_verification_required(allauth_email_view), name='account_email'),
    path('accounts/email/', login_required(ProtectedEmailView.as_view()), name='account_email'),
    path('email-verification/', include('email_verification.urls')),
    #path('register/', login_views.register, name='register'),
    #path('mapka/', login_views.mapka, name='mapka'),
    #path('login/', login_views.login, name='login'),
    path('privacy-policy/', login_views.privacy_policy, name='privacy_policy'),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/main/')), # root URL redirect
    path('main/', include('main.urls')),
    path('', include('texts.urls', namespace='texts')),
    path('', include('search.urls', namespace='search')),
    path('', include('user_profile.urls', namespace='user_profile')),
    path('', include('add_product_main.urls', namespace='add_product_main')),
    path('', include('edit_profile.urls', namespace='edit_profile')),
    path('', include('chat_polozka.urls', namespace='chat_polozka')),
    path('', include('obrazky.urls', namespace='obrazky')),
    path('', include('chat_general.urls', namespace='chat_general')),
    path('email-verification/', include('email_verification.urls')),
    # URL pattern for serving static files in development
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
