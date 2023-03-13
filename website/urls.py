import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include("django.contrib.auth.urls")),
    path('payment/', include('payment.urls')),
    path('verification/', include('verify_email.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import mimetypes

    import debug_toolbar

    mimetypes.add_type("application/javascript", ".js", True)
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
