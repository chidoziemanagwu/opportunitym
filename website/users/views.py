import os
from pickle import EMPTY_LIST, EMPTY_SET
from queue import Empty
import time
import uuid
from pathlib import Path

from base.views import get_client_ip
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import (login_required,
                                            permission_required,
                                            user_passes_test)
from django.contrib.auth.models import Group, User, auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.db.models.signals import post_init, post_save, pre_delete
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.urls import reverse
from dotenv import load_dotenv
from payment.stripe_API import (create_account, create_account_link,
                                create_login_link)
from verify_email.email_handler import send_verification_email

from .decorators import allowed_users, unauthenticated_user
from .forms import (CustomUserCreationForm, PasswordChangeForm, ProfileForm,
                    UserProfileUpdateForm)
from .models import Profile, Stripe_account

# from users.forms import CustomUserCreationForm


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_path = Path(BASE_DIR / 'website/.env')
load_dotenv(dotenv_path=dotenv_path)

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')

# print(Group.objects.all())
# print(len(Group.objects.all()))

try:
    if len(Group.objects.all()) == 0:
        group_list = ['basic', 'speaker', 'organiser']
        for x in group_list:
            create_group = Group(name=x)
            create_group.save()
except:
    print("No Database in the project")


def dashboard(request):
    return render(request, "users/dashboard.html")

def settings_(request):
    return render(request, "users/settings.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":

        stripe_account = Stripe_account()
        unix_datetime = round(time.time())
        user_ip_address = get_client_ip(request)
        form = CustomUserCreationForm(request.POST)
        current_user = request.user

        # new_user = User.objects.create_user(username='test_user_in_backend',
        #                          email='jlennon@beatles.com',
        #                          password='glass onion')

        # new_user.save()

        if form.is_valid():
            user = form.save()

            firstName = str(request.POST.get("first_name"))
            lastName = str(request.POST.get("last_name"))
            random_uuid = str(uuid.uuid1())

            username =firstName+lastName+random_uuid 
            print(username)

            user.username = username

            user.save()            
            login(request, user)
            print("working!!!!!!!")
            email = (request.POST.get("email"))

 
            # print(type(email))
            # print(type(user_ip_address))
            # print(form)

            stripe_id = create_account(STRIPE_SECRET_KEY, email, unix_datetime, user_ip_address)
            print(stripe_id)

            # save the data to database
            stripe_account.user = current_user
            stripe_account.stripe_id = stripe_id

            stripe_account.save()
            try:
                inactive_user = send_verification_email(request, form) #temporary removed
                print(inactive_user)   
            except:
                print("not working ")
            
            return redirect('activate')
        else:
            print("error")
            print(form.errors)
            return render(
                request, "registration/register.html",
                {"form": form}
            )
            # user = form.save()
            # login(request, user)
            # return redirect("/")

def linkexpired(request): 
    return render(request, 'registration/linkexpired.html')

def emailtemplate(request): 
    return render(request, 'registration/verification_email_template.html')

def success_email(request): 
    return render(request, 'registration/success_email.html')

def activate(request):    
    return render(request, 'registration/activate.html')

def fail_verification(request):    
    return render(request, 'registration/fail_verification.html')

def resend_verification(request):    
    return render(request, 'registration/resend_verification.html')

def login_user(request):
    print("log in page")
    
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        try:
            username = User.objects.get(email=email).username
            print(username)
            user = auth.authenticate(username=username, password=password)
            print(user)


            if user is not None:
                auth.login(request, user)
                profile = Profile.objects.filter(user = request.user)
                # print(profile_list)
        
                #first-time user doesn't have a profile
                if not profile:
                    return redirect(f'/users/profile/{username}')
                # else: 
                #     return redirect('/')
                else:
                    user_profile = Profile.objects.get(user = request.user)
                    is_first = user_profile.firstTime_user
                    print(is_first == False)
                    
                    #first time user checker
                    if is_first == True:
                        is_first = False
                        user_profile.save()
                        return redirect(f'/users/profile/{username}')

                    else:
                        return redirect('/')

            else:
                messages.info(request, 'Invalid Username or Password')
                return redirect('user_login_page')

        except:
            print("missing User")
            messages.info(request, 'Invalid Username or Password')
            return redirect('user_login_page')   
               
    else:
        return render(request, 'registration/login.html')


@receiver(pre_delete, sender=Profile)
def delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.profile_pic_URL.delete(False)


@receiver(post_init, sender=Profile)
def file_path(sender, instance, **kwargs):
    instance.saved_pic = instance.profile_pic_URL
    instance.saved_video = instance.bio_video_URL


@receiver(post_save, sender=Profile)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, 'saved_pic'):
        if instance.saved_pic != instance.profile_pic_URL:
            instance.saved_pic.delete(save=False)
    if hasattr(instance, 'saved_video'):
        if instance.saved_video != instance.bio_video_URL:
            instance.saved_video.delete(save=False)


def profile(request, username_profile):
    print("testing")
    users_list = User.objects.all()
    # username_profile = 'username1'
    user = User.objects.filter(id=request.user.id)
    current_user = request.user

    users_profile = Profile.objects.filter(user_id=current_user.id)
    print(current_user)
    # print(users_profile)
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        print("Profile does not exist")
        print("Creating a new profile")
        user_profile = Profile(user=request.user)
        user_profile.save()


    if "password" in request.POST:
        username = request.user
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user_auth = auth.authenticate(username=username, password=old_password)
        data = {
            'old_password': old_password, 'new_password1': new_password, 'new_password2': new_password
        }
        password_change_form = PasswordChangeForm(request.user, data)

        if user_auth is not None and password_change_form.is_valid():
            # user.set_password(new_password)
            # user.save()
            password_change_form.save()
            messages.success(request, "please login again")
            return redirect('user_login_page')
        else:
            print(password_change_form.errors)
            return render(
                request,
                "users/your_profile.html",
                {"form": password_change_form}
            )
            # messages.success(request, password_change_form.errors)

    elif "stripe_button" in request.POST:
        print("stripe section")
        current_user = request.user
        try:
            stripe_account_id = Stripe_account.objects.get(user=current_user)
            print(stripe_account_id)
            stripe_link = create_account_link(
                STRIPE_SECRET_KEY, str(stripe_account_id))
            print(stripe_link)

            return redirect(stripe_link)

        except:
            print("no user")
    else:
        print("update section")
        if request.method == "POST":
            try:
                user_form = UserProfileUpdateForm(
                    request.POST, instance=request.user)
            except ObjectDoesNotExist:
                user_form = UserProfileUpdateForm(request.POST)

            try:
                profile_form = ProfileForm(
                    request.POST, request.FILES, instance=request.user.profile)
            except ObjectDoesNotExist:
                profile_form = ProfileForm(request.POST, request.FILES)


            if profile_form.is_valid() and user_form.is_valid():
                user_form.save()
                profile_form.save()

                # !replace dynamic url
                return redirect("/users/profile_info/" + username_profile)


            else:
                print("error")
                print(profile_form.errors)
                print(user_form.errors)

    if len(user) <= 0:
        print('user is null')
        messages.success(request, "please login again")
        return redirect('login_page')

    if len(users_profile) <= 0:
        print('profile is null')

        return render(request, 'users/your_profile.html',
                      {'title': "profile",
                       'users_list': users_list,
                       'user': user[0]})

    content = {'title': "profile",
               'users_list': users_list,
               'user': user[0],
               'profile': users_profile[0],
               }
    return render(request, 'users/your_profile.html', content)

    
#function to test user groups
def not_in_user_group(User):
    list_groups = ["admin","basic","speaker"]
    if User:
        return (lambda u:u.groups.filter(name__in=list_groups).count()== 0)
    return False


@login_required
@user_passes_test(not_in_user_group)
# @allowed_users(allowed_groups= ['admin','speaker'])
def profile_info(request, username_profile):
    user = User.objects.filter(id=request.user.id)
    try:
        users_profile = Profile.objects.filter(user_id=request.user.id)
    except Profile.DoesNotExist:
        redirect(f'/users/profile/{user.username}')
    current_user = request.user
    try:
        stripe_account = Stripe_account.objects.get(user=request.user)

    except Exception as e:
        print(e)
    stripe_link = ""
    stripe_ac_link = ""
    

    try:
        print(stripe_account.stripe_id)
        stripe_ac_link = (create_login_link(
            STRIPE_SECRET_KEY, stripe_account.stripe_id))
    except:
        print("User haven't fully create the account please go to update profile to register the stipe account ")
        
        stripe_ac_link = ""
        # return redirect("/404")
        try:
            stripe_account_id = Stripe_account.objects.get(user=current_user)
            print(stripe_account_id)
            stripe_link = create_account_link(
                STRIPE_SECRET_KEY, str(stripe_account_id))
            print(stripe_link)



        except:
            print("no user") 

    
    if len(user) <= 0:
        print('user is null')
        messages.success(request, "please login again")
        return redirect('login_page')

    if len(users_profile) <= 0:
        messages.error(
            request, "no profile for this user, please update or add profile first")
        
        messages.error(
            request, "Organiser will not see you if you haven't finished you profile")
        
        return redirect(f'/users/profile/{current_user.username}')

    content = {'title': "profile_info",
               'user': user[0],
               'profile': users_profile[0],
               'stripe_ac_link': stripe_ac_link,
               'stripe_link':stripe_link
               }

    return render(request, 'users/profile_info.html', content)
