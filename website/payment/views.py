# Create your views here.
import os

from base.models import Marketplace, speaker_applied_event
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.base import TemplateView
from dotenv import load_dotenv
from paypal.standard.forms import PayPalPaymentsForm
from requests import session
from users.models import Profile, Stripe_account

from .models import Price, Product, payment_detail
from .stripe_API import *

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(BASE_DIR / 'website/.env')
load_dotenv(dotenv_path=dotenv_path)

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')
STRIPE_TEST_ENDPOINT_SECRET = os.getenv('STRIPE_TEST_ENDPOINT_SECRET')

####################################################################################
class HomePageView(TemplateView):
    template_name = 'payment/landing.html'

    def get_context_data(self, **kwargs):
        product = Product.objects.get(name="product 1")
        prices = Price.objects.filter(product=product)
        context = super(HomePageView,
                        self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "prices": prices
        })
        return context


class SuccessView(TemplateView):
    template_name = 'payment/payment_success.html'


class CancelledView(TemplateView):
    template_name = 'payment/payment_cancel.html'


def create_checkout_session(request):

    price_id = "price_1LLUZMIoOYLVzWlCq3m9JDf6"
    # success_url = "http://127.0.0.1:8000/payment/success"
    # cancel_url = "http://127.0.0.1:8000/payment/cancel" #localhost:3000
    success_url = "https://opportunitym.com/payment/success"
    cancel_url = "https://opportunitym.com/payment/cancel" #localhost:3000
    url = (create_payment_session(STRIPE_SECRET_KEY,
           price_id, success_url, cancel_url)["url"])

    return redirect(url)

@login_required
def accepting_payment(request):
    try:
        users_profile = Profile.objects.all()
    except:
        print("Profile database are missing")
        return redirect("/404")

    current_user = request.user

    try:
        # event host by organizers
        event_host_by_organiser = Marketplace.objects.filter(
            Creator=current_user)
    except:
        print("Marketplace database is missing")
        return redirect("/404")

    dictionary_event = {}
    speaker_list = []

    for x in range(len(event_host_by_organiser)):
        # print(event_host_by_organiser[x].Speaking_Event_Name)
        query = speaker_applied_event.objects.filter(
            event=event_host_by_organiser[x])
        speaker_list = []

        for y in range(len(query)):
            # print(query[y].user)
            speaker_list.append(query[y].user)

        dictionary_event[event_host_by_organiser[x].Speaking_Event_Name] = speaker_list

    print(dictionary_event)

    if "userID" in request.POST:
        product_id = Organiser_to_Speaker_product_id

        user_id = (request.POST.get("userID"))
        # print(user_id)
        event_name = request.POST.get("event_name")
        # print(event_name)

        event = Marketplace.objects.get(Speaking_Event_Name=event_name)
        event_worth = (event.Worth)

        User = get_user_model()
        selected_user = User.objects.get(id=user_id)

        # print(selected_user)

        try:

            stripe_account_id = Stripe_account.objects.get(user=selected_user)
            # print("stripe_account_id")
            # print(stripe_account_id)

        except:
            print("missing stripe_account_id for that user please check database")
            return redirect("/404")

        # print(stripe_account_id)

        amount_to_paid = float(event_worth)
        amount_to_paid_in_pence = amount_to_paid*100
        amount_to_paid_in_pence = (int(amount_to_paid_in_pence))

        price_id = (create_price(STRIPE_SECRET_KEY,
                    amount_to_paid_in_pence, product_id)["id"])
        # print(price_id)

        # success_url = "http://localhost:3000/payment/success"
        success_url = request.build_absolute_uri('/payment/success/')
        # cancel_url = "http://localhost:3000/payment/cancel"
        cancel_url = request.build_absolute_uri('/payment/cancel/')

        commission = amount_to_paid_in_pence * 0.1
        # print("commission in_pence")
        # print(commission)

        stripe_fee = amount_to_paid_in_pence * 0.031
        # print("stripe_fee in_pence")
        # print(stripe_fee)

        application_fee_amount = int(commission + stripe_fee)
        # print("application_fee_amount in_pence")
        # print(application_fee_amount)

        payment_session = create_payment_session(
            STRIPE_SECRET_KEY, price_id, success_url, cancel_url, stripe_account_id, application_fee_amount)
        # print(payment_session)

        payment_intent_id = payment_session["payment_intent"]
        # print("payment_intent_id")
        # print(payment_intent_id)

        url = (payment_session["url"])

        return redirect(url)

    content = {
        "dictionary_event": dictionary_event,
        "users_profile": users_profile,
        "title": "accepting payment"
    }

    return render(request, "payment/accept_payment.html", content)


####################################################################################
# * Testing Dynamic URL Patterns


@login_required
def accepting_payment_dynamic_url(request,event_id):

    print(event_id)

    try:
        users_profile = Profile.objects.all()
    except:
        print("Profile database are missing")
        return redirect("/404")

    current_user = request.user

    try:
        # event host by organizers
        event_host_by_organiser = Marketplace.objects.filter(
            Creator=current_user)
    except:
        print("Marketplace database is missing")
        return redirect("/404")

    dictionary_event = {}
    speaker_list = []

    print("The len value for this event is " + str(len(event_host_by_organiser)))
    print(event_host_by_organiser)

    for x in range(len(event_host_by_organiser)):
        str_event_host_by_organiser_id = (str(event_host_by_organiser[x].id))
        print(str_event_host_by_organiser_id)

        if str_event_host_by_organiser_id == event_id:
            
            query = speaker_applied_event.objects.filter(
                event=event_host_by_organiser[x])
            # print(query)
            speaker_list = []

            for y in range(len(query)):
                # print(query[y].user)
                speaker_list.append(query[y].user)

            dictionary_event[event_host_by_organiser[x].Speaking_Event_Name] = speaker_list

    print(dictionary_event)

    if "userID" in request.POST:
        product_id = Organiser_to_Speaker_product_id

        user_id = (request.POST.get("userID"))
        # print(user_id)
        event_name = request.POST.get("event_name")
        # print(event_name)

        event = Marketplace.objects.get(Speaking_Event_Name=event_name)
        event_worth = (event.Worth)

        User = get_user_model()
        selected_user = User.objects.get(id=user_id)

        # print(selected_user)

        try:

            stripe_account_id = Stripe_account.objects.get(user=selected_user)
            # print("stripe_account_id")
            # print(stripe_account_id)

        except:
            print("missing stripe_account_id for that user please check database")
            return redirect("/404")

        # print(stripe_account_id)

        amount_to_paid = float(event_worth)
        amount_to_paid_in_pence = amount_to_paid*100
        amount_to_paid_in_pence = (int(amount_to_paid_in_pence))

        price_id = (create_price(STRIPE_SECRET_KEY,
                    amount_to_paid_in_pence, product_id)["id"])
        # print(price_id)

        # success_url = "http://localhost:3000/payment/success"
        success_url = request.build_absolute_uri('/payment/success/')
        # cancel_url = "http://localhost:3000/payment/cancel"
        cancel_url = request.build_absolute_uri('/payment/cancel/')

        commission = amount_to_paid_in_pence * 0.1
        # print("commission in_pence")
        # print(commission)

        stripe_fee = amount_to_paid_in_pence * 0.031
        # print("stripe_fee in_pence")
        # print(stripe_fee)

        application_fee_amount = int(commission + stripe_fee)
        # print("application_fee_amount in_pence")
        # print(application_fee_amount)

        payment_session = create_payment_session(
            STRIPE_SECRET_KEY, price_id, success_url, cancel_url, stripe_account_id, application_fee_amount)
        # print(payment_session)

        payment_intent_id = payment_session["payment_intent"]
        # print("payment_intent_id")
        # print(payment_intent_id)

        url = (payment_session["url"])

        return redirect(url)

    content = {
        "dictionary_event": dictionary_event,
        "users_profile": users_profile,
        "title": "accepting payment"
    }

    return render(request, "payment/accept_payment.html", content)



####################################################################################

def store_payment_details(is_paid, event):
    """storing date from webhook to database

    Keyword arguments:
    is_paid -- paid or not
    event -- event get form webhook
    Return: nothing to return
    """

    stripe_id = event["data"]["object"]["charges"]["data"][0]["destination"]
    payment_intent_id = event["data"]["object"]["charges"]["data"][0]["payment_intent"]

    print(stripe_id)
    print(payment_intent_id)

    try:
        get_payment_detail_db = payment_detail.objects.get(
            payment_intent_id=payment_intent_id)

        if get_payment_detail_db != None:
            print("already have record need to update database")
            print(get_payment_detail_db)
            get_payment_detail_db.payment_status = is_paid
            get_payment_detail_db.save()

    except:
        print("cannot find that payment details in database so create it now")

        payment_detail_db = payment_detail()
        payment_detail_db.stripe_id = stripe_id
        payment_detail_db.payment_intent_id = payment_intent_id
        payment_detail_db.payment_status = is_paid
        payment_detail_db.save()


@require_POST
@csrf_exempt
def stripe_webhook(request):

    stripe.api_key = STRIPE_SECRET_KEY
    endpoint_secret = STRIPE_ENDPOINT_SECRET

    # print(endpoint_secret)
    payload = request.body.decode('utf-8')

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:

        print("Invalid payload")
        html = "<html><body><h1>Invalid payload</h1></body></html>"
        return HttpResponse(html,status=400)
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature")
        html = "<html><body><h1>Invalid signature</h1></body></html>"
        return HttpResponse(html,status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'payment_intent.succeeded':
        print("Payment was successful.")
        is_paid = True
        store_payment_details(is_paid, event)

    elif event['type'] == 'payment_intent.payment_failed':
        print("Payment was failed.")
        is_paid = False
        store_payment_details(is_paid, event)

    return HttpResponse(status=200)

####################################################################################


def paypal_process_payment(request):
    # order_id = request.session.get('order_id')
    # order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': 30,
        'item_name': "item1",
        'invoice': "invoice1",
        'currency_code': 'GBP',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal_return")}',
        'cancel_return': f'http://{host}{reverse("paypal_cancel")}',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    content = {
        'form': form
    }
    return render(request, 'test.html', content)


def paypal_return(request):
    messages.success(request, "success")
    return redirect("/")


def paypal_cancel(request):
    messages.success(request, "fail")
    return redirect("/")
