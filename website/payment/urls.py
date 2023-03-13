import stripe
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import include, path

from .views import *

urlpatterns = [

    # * version 3
    path('accepting_payment/',accepting_payment,name='accepting_payment'),
    path('create_checkout_session/',create_checkout_session,name="create_checkout_session"),
    path('success/', SuccessView.as_view(),name = "success"), 
    path('cancel/',CancelledView.as_view(),name='cancel'),  
    path('webhook/', stripe_webhook,name = "stripe_webhook"), 
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('accepting_payment2/<str:event_id>',accepting_payment_dynamic_url,name='accepting_payment'),


    # path('paypal_process_payment/',paypal_process_payment,name="paypal_process_payment"),
    # path('paypal_return/',paypal_return,name="paypal_return"),
    # path('paypal_cancel/',paypal_cancel,name="paypal_cancel"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
