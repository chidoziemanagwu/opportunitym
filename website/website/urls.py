import debug_toolbar
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.static import serve

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secretAdminPage/', admin.site.urls),
    path('', include('base.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('payment/', include('payment.urls')),
    path('verification/', include('verify_email.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    #RESET PASSWORD
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_pwd/reset_password.html",html_email_template_name="reset_pwd/resetpwd_template_email.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_pwd/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset_pwd/reset_password_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_pwd/reset_password_complete.html"), name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import mimetypes

    import debug_toolbar

    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
