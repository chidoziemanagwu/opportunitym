from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import include, path

from .views import *

urlpatterns = [
                  path('dashboard/', dashboard, name="dashboard"),
                  path('register/', register, name="register"),
                  path('login/', login_user, name="user_login_page"),
                  path('verification/', include('verify_email.urls'), name="verification"),	
                  path('activate/', activate, name="activate"), #temporary
                  path('resend_verification/', resend_verification, name="resend_verification"), #temporary
                  path('success_email/', success_email, name="success_email"),  #temporary
                  path('emailtemplate/', emailtemplate, name="emailtemplate"), #temporary
                  path('linkexpired/', linkexpired, name="linkexpired"), #temporary
                  # path('profile/', profile, name='Your_profile'),
                  # path('verification_email_template/', verification_email_template, name="verification_email_template"),
                  path('profile/<str:username_profile>/', profile, name='Your_profile'),
                  path('profile_info/<str:username_profile>/', profile_info, name='profile_info'),
                  path('settings/', settings_, name='settings'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
