import os
from ipaddress import ip_address
from multiprocessing import context
from pathlib import Path
from telnetlib import STATUS
from warnings import catch_warnings

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Case, When, Value
# from Website_repo.website.users.decorators import allowed_users
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import HttpResponse
from users.models import Profile
from payment.stripe_API import create_login_link, create_account_link, STRIPE_SECRET_KEY

from website.test_db_connection import isConnected
from users.models import Profile, Stripe_account

import requests
import json
import re

from .decorators import allowed_users, unauthenticated_user
from .forms import Marketplace_form, PostForm, JobPost_form
from .models import Events_topic, Marketplace, Post, speaker_applied_event, EventStatus, TeamMember, Opportunity_suggestion, Opportunity_suggestion_user_data, Newsletter_email, Opportunity_Portfolio_mailing_list, Opportunity_Verified_mailing_list, Job_post, seeker_applied_job, JobPostStatus, JobMode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from datetime import datetime

BASE_DIR = str(Path(__file__).resolve().parent.parent)

# print(BASE_DIR + 'static/images/about_page_logo')
about_page_img = []
for file in os.listdir(BASE_DIR + '/static/images/about_page_logo'):
    file = 'images/about_page_logo/' + file
    about_page_img.append(file)
about_page_img.sort()

User = get_user_model()
users_list = User.objects.all()

# * getting the data from database

try:
    event_details = Marketplace.objects.all()
    job_details = Job_post.objects.all()
except:
    print("outside")
    print("Missing Marketplace table in database ")
    print("Please make migrations and restart the web app")

# @login_required
# @allowed_users(allowed_groups=['admin','speaker','basic'])
def index(request):
    content = {'title': "Unlock Your Potential with OpportunityM: Empowering Your Career and Personal Growth"}
    try:
        if isConnected:
            return render(request, 'index.html', content)
    except:
        print("last")
        print("isConnected set to False")
        print("Please ensure that isConnected is True")
        return redirect("/404")

def submit_interest_for_opp_portfolio(request):
    if request.method == "POST":
        opportunity_portfolio_name = request.POST["opportunity_portfolio_name"]
        opportunity_portfolio_email = request.POST["opportunity_portfolio_email"]
        opportunity_portfolio_company = request.POST["opportunity_portfolio_company"]
        if Opportunity_Portfolio_mailing_list.objects.filter(email=opportunity_portfolio_email).exists():
            success_add_email1 = 'Looks like you have already signed up.'
            return HttpResponse(success_add_email1)
        else:
            try:
                html_content = render_to_string("opportunity_portfolio_signup_email.html", {
                    'name': opportunity_portfolio_name.split()[0]
                })
                text_content = strip_tags(html_content)
                email_reciever = opportunity_portfolio_email
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    "Opportunity Portfolio Email",
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                add_email_to_opp_portfolio_mailinglist = Opportunity_Portfolio_mailing_list(email=opportunity_portfolio_email, name=opportunity_portfolio_name, company=opportunity_portfolio_company)
                add_email_to_opp_portfolio_mailinglist.save()
                success_add_email1 = "You've been swiftly sent an email with more info - did it come through okay? :)"

                return HttpResponse(success_add_email1)

            except:
                return HttpResponse("An error occured when submitting this form")

def submit_interest_for_opp_verified(request):
    if request.method == "POST":
        opportunity_verified_name = request.POST["opportunity_verified_name"]
        opportunity_verified_email = request.POST["opportunity_verified_email"]
        opportunity_verified_company = request.POST["opportunity_verified_company"]
        if Opportunity_Portfolio_mailing_list.objects.filter(email=opportunity_verified_email).exists():
            try:
                html_content = render_to_string("opportunity_verified_signup_email.html", {
                    'name': opportunity_verified_name.split()[0]
                })
                text_content = strip_tags(html_content)
                email_reciever = opportunity_verified_email
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    "Opportunity Verified Email",
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                # add_email_to_opp_portfolio_mailinglist = Opportunity_Portfolio_mailing_list(email=opportunity_portfolio_email, name=opportunity_portfolio_name, company=opportunity_portfolio_company)
                # add_email_to_opp_portfolio_mailinglist.save()
                success_add_email2 = "You've been swiftly sent an email with more info - did it come through okay? :)"

                return HttpResponse(success_add_email2)

            except:
                return HttpResponse("An error occured when submitting this form")
        
        else:
            success_add_email2 = 'This product is only for customers who have registered for Opportunity Portfolio'
            return HttpResponse(success_add_email2)

def add_opportunity(request):
    if request.method == "POST":
        opportunity_user_id = request.POST["opportunity_user_id"]
        opportunity_sub = request.POST["opportunity"].lower()
        opportunity_firstname = request.POST["opportunity_firstname"]
        opportunity_email = request.POST["opportunity_email"]
        
        opportunity_region = request.POST["opportunity_region"]
        opportunity_checkbox = request.POST["opportunity_checkbox"]

        ip = requests.get('https://api.ipify.org?format=json')
        ip_data = json.loads(ip.text)
        res = requests.get('http://ip-api.com/json/' + ip_data["ip"])
        # res = requests.get('http://ip-api.com/json/24.48.0.1') #dummy ip address for testing
        location_data_one = res.text
        location_data = json.loads(location_data_one)

        getRegionName = location_data["regionName"]
        getCountryCode = location_data["countryCode"]
        getCity = location_data["city"]

        if opportunity_user_id != "-":
            get_user_profile = Profile.objects.filter(user=request.user)
            if get_user_profile[0].Phone_number == "None":
                opportunity_telephone = ""
            else:
                opportunity_telephone = get_user_profile[0].Phone_number
        else:
            opportunity_telephone = request.POST["opportunity_telephone"]

        if Opportunity_suggestion_user_data.objects.filter(user_id=opportunity_user_id, firstname=opportunity_firstname, email=opportunity_email, telephone=opportunity_telephone, opportunity=opportunity_sub, desired_region=opportunity_region).exists():
            try:
                return HttpResponse('<p style="color: orange">You have already submited this opportunity</p>')
            except:
                return HttpResponse('<p style="color: red">An error occured while filtering opportunity details</p>')
        else:
            if opportunity_region == "Choose":
                return HttpResponse('<p style="color: red">Please select a region</p>')
            else:
                if opportunity_checkbox == "true":
                    new_user_data = Opportunity_suggestion_user_data(user_id=opportunity_user_id, firstname=opportunity_firstname, email=opportunity_email, telephone=opportunity_telephone, opportunity=opportunity_sub, country=getRegionName, desired_region=opportunity_region, countrycode=getCountryCode, city=getCity)
                    new_user_data.save()
                else:
                    new_user_data = Opportunity_suggestion_user_data(user_id=opportunity_user_id, firstname=opportunity_firstname, email=opportunity_email, telephone=opportunity_telephone, opportunity=opportunity_sub, desired_region=opportunity_region)
                    new_user_data.save()
                    
                if Opportunity_suggestion.objects.filter(opportunity=opportunity_sub).exists():
                    get_opportunity = Opportunity_suggestion.objects.get(opportunity=opportunity_sub)
                    get_opportunity.count = get_opportunity.count + 1
                    get_opportunity.save(update_fields=["count"])
                    print(get_opportunity)
                    success_new_opportunity1 = str(get_opportunity.count) + ' people have registered interest in ' + opportunity_sub + ' so far'
                    return HttpResponse(success_new_opportunity1)
                else:
                    print("this opportunity is new")
                    new_opportunity = Opportunity_suggestion(opportunity=opportunity_sub)
                    new_opportunity.save()
                    print(new_opportunity)
                    success_new_opportunity2 = opportunity_sub + ' has been added to our list of opportunities'
                    return HttpResponse(success_new_opportunity2)

def subscribe_to_newsletter(request):
    if request.method == "POST":
        add_email = request.POST["newsletter"]
        firstname = request.POST["newsletter_firstname"]
        if Newsletter_email.objects.filter(email=add_email).exists():
            email_exists = "Looks like you're already subscribed to our newsletter"
            print(Newsletter_email.objects.filter(email=add_email)[0].id)
            return HttpResponse(email_exists)
        else:
            try:
                add_email_to_mailinglist = Newsletter_email(email=add_email)
                add_email_to_mailinglist.save()
                email_id = Newsletter_email.objects.filter(email=add_email)[0].id
                print(email_id)
                html_content = render_to_string("newsletter_email.html", {
                    'name': firstname,
                    'email_id': email_id,
                })
                text_content = strip_tags(html_content)
                email_reciever = add_email
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    "You have successfully subscribed to our monthly newsletter",
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                success_add_email = 'You have been added to our monthly newsletter mailing list'
                return HttpResponse(success_add_email)
            except:
                return HttpResponse('An error has occured when adding your email to our system')

def unsubscribe_to_newsletter(request, email_id):
    if Newsletter_email.objects.filter(id=email_id).exists():
        if request.method == 'POST':
            if 'unsubscribe' in request.POST:
                Newsletter_email.objects.filter(id=email_id).delete()
                content = {'title': "Unsubscribe from OpportunityM's mailing list", 'state': 'justunsubscribed'}
                return render(request, 'unsubscribe_page.html', content)
        content = {'title': "Unsubscribe from OpportunityM's mailing list", 'state': 'subscribed'}
        return render(request, 'unsubscribe_page.html', content)
    else:
        content = {'title': "Unsubscribe from OpportunityM's mailing list", 'state': 'unsubscribed'}
        return render(request, 'unsubscribe_page.html', content)

def about(request):
    try:
        teamMemberList = TeamMember.objects.all()
    except:
        print("Missing speaker_applied_event table in database")
        print("Please make migrations and restart the web app")
        return redirect("/404")
    content = {'title': "about us",
               'about_page_img': about_page_img,
               'teamMembers': teamMemberList,
               }
    return render(request, 'about.html', content)

def opportunity_board(request):
    content = {'title': "opportunity_board"}
    return render(request, 'opportunity_board.html', content)

#function to test user groups
def not_in_user_group(user):
    list_groups = ["admin","basic","speaker"]
    if user:
        return (lambda u:u.group.filter(name__in=list_groups).count()== 0)
    return False


#--------------------------------------------------------------------------------------------------------------------------------------
# @login_required(login_url='/users/login')
# @user_passes_test(not_in_user_group)
# @allowed_users(allowed_groups=['speaker','admin','basic'])
def speakers(request):
    try:
        current_user = request.user
        event_details = [event for event in Marketplace.objects.all() if event.Status is not EventStatus.Completed and event.Status is not EventStatus.Archived]
        Speaker_applied_event = speaker_applied_event()
        # example = event_details
        # print(type(example))
    except:
        print("Missing Marketplace table in database")
        print("Please make migrations and restart the web app")
        event_details = {}
        return redirect("/404")

    content = {'title': "speakers",
               'events': event_details,
               'message': "to view events",
               }
    # print(content)

    if request.method == 'POST':
        if 'Apply' in request.POST:
            if not request.user.is_staff:
                #check if user had fully created a stripe account
                try:
                    stripe_account = Stripe_account.objects.get(user=request.user)
                    stripe_ac_link = (create_login_link(
                        STRIPE_SECRET_KEY, stripe_account.stripe_id))

                except:
                    print("User haven't fully create the account please go to update profile to register the stipe account ")
                    stripe_link = create_account_link(
                    STRIPE_SECRET_KEY, str(stripe_account))
                    print(stripe_link)
                    return redirect(stripe_link)

            
            user_id_for_selecting_event = request.POST.get("user_id")
            event_id_user_selected = request.POST.get("event_id")
            User_obj = User.objects.get(pk=user_id_for_selecting_event)
            Event_obj = Marketplace.objects.get(pk=event_id_user_selected)

            Speaker_applied_event.user = User_obj
            Speaker_applied_event.event = Event_obj

            Speaker_applied_event.save()

            try:
                user_group = Group.objects.get(name="speaker")
                user_group.user_set.add(current_user)

            except:
                print("No user group assigned")
        elif 'Unapply' in request.POST:
            event_id = request.POST.get("event_id")
            target_event = Marketplace.objects.get(pk=event_id)
            applied_event = speaker_applied_event.objects.filter(event=target_event, user=request.user)
            applied_event.delete()

    try:
        if isConnected:
            return render(request, 'speakers.html', content)
    except:
        print("last")
        print("missing database")
        print("Please make migrations and restart the web app")
        return redirect("/404")

def find_jobs(request):
    try:
        # current_user = request.user
        # job_details = [job_position for job_position in Job_post.objects.all() if job_position.Status is not JobPostStatus.Closed]
        job_details = Job_post.objects.all()
        Seeker_applied_job = seeker_applied_job()
        # example = job_details
        # print(JobPostStatus.Open)
        # print(example)
        # print(type(example))
        
    except:
        print("Missing Job_post table in database")
        print("Please make migrations and restart the web app")
        job_details = {}
        return redirect("/404")

    content = {'title': "Job seekers", 
                'jobs': job_details, 
                'message': "to view job postings"}
    print(content)

    if request.method == 'POST':
        if 'Apply' in request.POST:
            user_id_for_selecting_job = request.POST.get("user_id")
            job_id_user_selected = request.POST.get("job_id")
            User_obj = User.objects.get(pk=user_id_for_selecting_job)
            Job_obj = Job_post.objects.get(pk=job_id_user_selected)

            Seeker_applied_job.user = User_obj
            Seeker_applied_job.job_position = Job_obj

            Seeker_applied_job.save()

        elif 'Unapply' in request.POST:
            job_id = request.POST.get("job_id")
            target_job = Job_post.objects.get(pk=job_id)
            applied_job = seeker_applied_job.objects.filter(job_position=target_job, user=request.user)
            applied_job.delete()

    try:
        if isConnected:
            return render(request, 'seek_job.html', content)
    except:
        print("last")
        print("missing database")
        print("Please make migrations and restart the web app")
        return redirect("/404")

def create_jobs(request):
    try:
        users_list = User.objects.all()
        # getting the current user
        current_user = request.user
        job_list = Job_post.objects.filter(Creator=current_user).order_by(Case( 
                        When(Status="Open", then=Value(0)),
                        When(Status="Closed", then=Value(1)),
                        )
                    )
        print(job_list)
    except:
        # print("Missing Marketplace table in database")
        # print("Please make migrations and restart the web app")
        # event_list = {}
        # return redirect("/404")
        content = {'title': "Create job posting", 'message': "to add job posting",}
        return render(request, 'post_job.html', content)

    # getting the current user
    current_user = request.user
    form = JobPost_form()

    # print(Marketplace_form())
    if request.method == 'POST':
        print(request.POST)
        if 'Create_Job' in request.POST:
            print('start posting form')
            form = JobPost_form(request.POST, request.FILES)
            # try:
            #     user_group = Group.objects.get(name="organiser")
            #     user_group.user_set.add(current_user)
            # except:
            #     print("No user group assigned")

            print('form is:', form.is_valid())
            print(request.POST)
            if form.is_valid():
                print('successful')
                # print(form.fields["Deadline"])
                # print(form.cleaned_data["Deadline"])
                form.cleaned_data["Deadline"] = datetime.combine(form.cleaned_data["Deadline"].date(),
                                                            datetime.strptime("23:59", '%H:%M').time())
                # print(form.cleaned_data["Deadline"])
                form.save()
                print(form)
                # getPost = request.POST.get("Image_URL")
                # print(getPost)
                instance = Job_post.objects.get(Job_role=form.cleaned_data["Job_role"], Company=form.cleaned_data["Company"])
                instance.Deadline = form.cleaned_data["Deadline"]
                instance.save()
                print(instance)

            else:
                print('check')
                print(form.errors)
                content = {'title': "Create job posting",
                        "form": request.POST,
                        'jobs': job_list,
                        'users_list': users_list,
                        "errors": form.errors
                        }

                return render(request, 'post_job.html', content)

    content = {'title': "Create job posting",
               "form": form,
               'jobs': job_list,
               'users_list': users_list
               }
    
    if "see_all_applicants" in request.POST:
        job_id = request.POST.get("see_all_applicants")
        print(job_id)

        return redirect("/view_job_applicants/" + job_id)

    if "edit" in request.POST:
        job_id = request.POST.get("edit")
        print(job_id)
        return redirect("/edit_job/" + job_id)

    if 'delete' in request.POST:
        job_id = request.POST.get("delete")
        target_job = Job_post.objects.get(pk=job_id)
        applied_job = seeker_applied_job.objects.filter(job_position=target_job, user=request.user)
        applied_job.delete()
        get_job = Job_post.objects.filter(pk=job_id)
        get_job.delete()
        return redirect("/create_jobs")

    return render(request, 'post_job.html', content)

@login_required
def view_job_applicants(request, job_id):
    print(job_id)
    try:
        users_profile = Profile.objects.all()
    except:
        print("Profile database are missing")
        return redirect("/404")

    current_user = request.user
    
    try:
        job_by_job_poster = Job_post.objects.filter(
            Creator=current_user)
    except:
        print("Marketplace database is missing")
        return redirect("/404")

    dictionary_job = {}
    seeker_list = []

    for x in range(len(job_by_job_poster)):
        job_by_job_poster_id = (job_by_job_poster[x].id)
        print(job_by_job_poster_id)

        if job_by_job_poster_id == job_id:
            query = seeker_applied_job.objects.filter(job_position=job_by_job_poster[x])
            print(query)
            seeker_list = []

            for y in range(len(query)):
                print(query[y].user)
                seeker_list.append(query[y].user)

            dictionary_job[job_by_job_poster[x].Job_role] = seeker_list

    print(dictionary_job)
    
    content = {
        "dictionary_job": dictionary_job,
        "users_profile": users_profile,
        "title": "View applicants"
    }

    return render(request, "view_job_applicants.html", content)
#------------------------------------------------------------------------------------------------------------------------------------

def terms_and_conditions(request):
    content = {'title': "terms_and_conditions"}
    return render(request, 'terms-and-conditions.html', content)


def privacy_policy(request):
    content = {'title': "privacy_policy"}
    return render(request, 'privacy_policy.html', content)


def get_in_touch(request):
    content = {'title': "get_in_touch"}
    return render(request, 'get_in_touch.html', content)

def new(request):
    content = {'title': "new"}
    return render(request, 'new.html', content)

def book_oliver(request):
    if request.method == "POST":
        if 'submit_form' in request.POST:
            try:
                html_content = render_to_string("book_oliver_email.html", {
                        'title': 'Book Oliver submission',
                        'Firstname': request.POST.get('Firstname'),
                        'Lastname': request.POST.get('Lastname'),
                        'Email': request.POST.get('Email'),
                        'Url': request.POST.get('Url'),
                        'Tel' : request.POST.get('Tel'),
                        'Company': request.POST.get('Company'),
                        'JobTitle': request.POST.get('JobTitle'),
                        'Appearance': request.POST.get('Appearance'),
                        'AppearanceDetails': request.POST.get('AppearanceDetails'),
                        'Location': request.POST.get('Location'),
                        'Budget': request.POST.get('Budget'),
                        'Dateandtime': request.POST.get('Dateandtime'),
                    })
                text_content = strip_tags(html_content)
                email_reciever = "oliver@opportunitym.com"
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    request.POST.get('Firstname') + " " + request.POST.get('Lastname') + " wants to book you in for a " + request.POST.get('Appearance'),
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return render(
                    request, "book_oliver_form.html", {'title': "Success", 'message': "Thank you for filling in the form"}
                )

            except:
                return render(
                    request, "book_oliver_form.html", {'title': "Form submission error", "message": "An error occured when submitting the form"}
                )

    content = {'title': "book_oliver"}
    return render(request, 'book_oliver_form.html', content)

def coming_soon(request):
    if request.method == 'POST':
        if 'Submit_question' in request.POST:
            try:
                html_content = render_to_string("ask_question_email.html", {
                    'question': request.POST.get('question')
                })
                text_content = strip_tags(html_content)
                email_reciever = "oliver@opportunitym.com"
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    "You have a new question - " + request.POST.get('question'),
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return render(
                    request, "coming_soon.html", {'title': "Success", 'message': "Your question has been sent. We will get back to you shortly"}
                )

            except:
                return render(
                    request, "coming_soon.html", {'title': "Failed to send question", 'message': "An error occur while submitting your question"}
                )

    content = {'title': "coming soon"}
    return render(request, 'coming_soon.html', content)


def isOrganiser(user):
    return user.groups.filter(name='organiser').exists()

# @login_required(login_url='/users/login')
def launch_your_speaking_event(request):
    try:
        topics_list = Events_topic.objects.order_by('topic') #call the topic list
        users_list = User.objects.all()
        # getting the current user
        current_user = request.user
        event_list = Marketplace.objects.filter(Creator=current_user).order_by(Case( 
                            When(Status="Open", then=Value(0)),
                            When(Status="Closed", then=Value(1)),
                            When(Status="Completed", then=Value(2)),
                            When(Status="Archived", then=Value(3)),
                        )
                    )#.alias(priority=Case(*[When(Status=status, then=Value(i)) for i, status in EventStatus])).order_by('priority')
        print(event_list)
    except:
        # print("Missing Marketplace table in database")
        # print("Please make migrations and restart the web app")
        # event_list = {}
        # return redirect("/404")

        content = {'title': "launch your speaking event", 'message': "to add events",}
        return render(request, 'launch_your_speaking_event.html', content)

    # getting the current user
    current_user = request.user
    form = Marketplace_form()

    # print(Marketplace_form())
    if request.method == 'POST':
        print(request.POST)
        if 'Create_Event' in request.POST:
            print('start posting form')
            form = Marketplace_form(request.POST, request.FILES)
            try:
                user_group = Group.objects.get(name="organiser")
                user_group.user_set.add(current_user)
            except:
                print("No user group assigned")

            print('form is:', form.is_valid())
            print(request.POST)
            if form.is_valid():
                print('successful')
                print(form.fields["date"])
                print(form.cleaned_data["date"].time())
                form.cleaned_data["date"] = datetime.combine(form.cleaned_data["date"].date(),
                                                            datetime.strptime(request.POST.get("time"), '%H:%M').time())
                print(datetime.strptime(request.POST.get("time"), '%H:%M').time())
                print(form.cleaned_data["date"].time())
                form.save()
                instance = Marketplace.objects.get(Speaking_Event_Name=form.cleaned_data["Speaking_Event_Name"])
                instance.date = form.cleaned_data["date"]
                instance.save()
                print(instance.date)

            else:
                print('check')
                print(form.errors)
                content = {'title': "launch your speaking event",
                        "form": request.POST,
                        'events': event_list,
                        'users_list': users_list,
                        "isOrganiser": isOrganiser(current_user),
                        "errors": form.errors
                        }
                
                return render(request, 'launch_your_speaking_event.html', content)

    content = {'title': "launch your speaking event",
               "form": form,
               'events': event_list,
               'users_list': users_list,
               'topics_list': topics_list,
               "isOrganiser": isOrganiser(current_user)}

    if "see_all_applicants" in request.POST:
        event_id = request.POST.get("see_all_applicants")
        print(event_id)

        return redirect("/payment/accepting_payment2/" + event_id)

    elif "edit" in request.POST:
        event_id = request.POST.get("edit")
        print(event_id)
        return redirect("/edit_event/" + event_id)

    if 'delete' in request.POST:
        event_id = request.POST.get("delete")
        target_event = Marketplace.objects.get(pk=event_id)
        applied_event = speaker_applied_event.objects.filter(event=target_event, user=request.user)
        applied_event.delete()
        get_job = Marketplace.objects.filter(pk=event_id)
        get_job.delete()
        return redirect("/launch_your_speaking_event")

    return render(request, 'launch_your_speaking_event.html', content)


# Getting user ip address

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def test(request):
    print(ip_address)
    print(get_client_ip(request))
    return render(request, 'test.html')


def error404(request):
    content = {'title': "404"}
    return render(request, 'error_404.html', content)


def cookie_statement(request):
    content = {'title': "cookie"}
    return render(request, 'cookie_statements.html', content)

def contact_us(request):
    if request.method == "POST":
        if 'submit_form' in request.POST:
            try:
                html_content = render_to_string("query_email.html", {
                        'full_name': request.POST.get('full_name'),
                        'email': request.POST.get('email'),
                        'subject': request.POST.get('subject'),
                        'message': request.POST.get('message'),
                    })
                text_content = strip_tags(html_content)
                email_reciever = "oliver@opportunitym.com"
                # subject, content, from_email, to_email
                email = EmailMultiAlternatives(
                    "QUERY: " + request.POST.get('subject'),
                    text_content,
                    "no-reply@opportunitym.com",
                    [email_reciever],
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                return render(
                    request, "contact_us.html", {'title': "Success", 'message': 'Thank you for submitting this form. We will get back to you soon'}
                )

            except:
                return render(
                    request, "contact_us.html", {'title': "Form submission error", "message": 'We cannot send this form at the moment. Please try again later'}
                )

    content = {'title': "contact_us"}
    return render(request, 'contact_us.html', content)


# def profile(request):
#     content = {'title': "profile"}
#     return render(request, 'your_profile.html', content)


def archive(request):
    content = {'title': "archive"}
    return render(request, 'archive.html', content)


def news_page(request):
    post_list = Post.objects.all()
    content = {'title': "news",
               'post_list': post_list}
    return render(request, 'news.html', content)


@login_required(login_url='/users/login')
@user_passes_test(lambda curr_user: curr_user.is_superuser)
def modify_post(request, post_slug):
    if request.method == 'POST':
        if post_slug != 'new_post':
            form = PostForm(request.POST, instance=Post.objects.get(author=request.user, slug=post_slug))
            if form.is_valid():
                form.save()
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.author = request.user
                instance.save()
        return redirect('my_post')
    else:
        print(post_slug)
        if post_slug == 'new_post':
            form = PostForm()
        else:
            form = PostForm(instance=Post.objects.get(author=request.user, slug=post_slug))
    content = {'title': "modify post",
               'form': form,
               'post_slug': post_slug}
    return render(request, 'modify_post.html', content)


@login_required(login_url='/users/login')
@user_passes_test(lambda curr_user: curr_user.is_superuser)
def my_post(request):
    post_list = Post.objects.filter(author=request.user)
    if request.method == 'POST':
        print(request.POST)
        if 'Delete' in request.POST:
            print('Delete')
            selected_post = Post.objects.get(author=request.user, slug=request.POST.get('Delete'))
            selected_post.delete()
        elif 'Add' in request.POST:
            return redirect('modify_post', post_slug='new_post')
        elif 'Edit' in request.POST:
            return redirect('modify_post', post_slug=request.POST.get('Edit'))
        elif 'Mail' in request.POST:
            print("The post ID is: " + request.POST.get('Mail'))
            newsletter = Post.objects.get(id=request.POST.get('Mail'))
            newsletter.mailed = True
            newsletter.save()

            newsletter_body = newsletter.body
            remover = re.compile('<.*?>')
            clean_newsletter_body = re.sub(remover, '', newsletter_body)
            clean_newsletter_body2 = clean_newsletter_body[0 : 400] + "..." if len(clean_newsletter_body) > 400 else clean_newsletter_body

            mailing_list_emails = Newsletter_email.objects.all()

            for x in range(len(mailing_list_emails)):
                try:
                    print ("Email: " + str(mailing_list_emails[x].id))

                    html_content = render_to_string("monthly_newsletter_email.html", {
                            'title': newsletter.title,
                            'body': clean_newsletter_body2,
                            'slug': newsletter.slug,
                            'email_id': mailing_list_emails[x].id,
                        })
                    text_content = strip_tags(html_content)
                    email_reciever = mailing_list_emails[x].email
                    # subject, content, from_email, to_email
                    email = EmailMultiAlternatives(
                        "This month's newsletter: " + newsletter.title,
                        text_content,
                        "no-reply@opportunitym.com",
                        [email_reciever],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                except:
                    print("Cannot send to this email because it is invalid or does not exist")



    content = {'post_list': post_list}
    return render(request, 'my_post.html', content)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    content = {'post': post}
    return render(request, 'post_detail.html', content)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# def marketplace_card(request):
#     content = {'event_details': event_details}
#     return render(request, 'marketplace_card.html', content)


# def register(request):
#     content = {'title': "register"}
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#     return render(request, "register.html", content)

#edit event
def marketplace(request):
    content = {
        'title': "marketplace",
        "form": Marketplace_form(),

    }
    if request.method == 'POST':
        form = Marketplace_form(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            print('successful')
    return render(request, 'marketplace.html', content)


# def profile(request):
#     content = {'title': "profile"}
#     return render(request, 'your_profile.html', content)

@login_required
def specific_applicants(request):

    # users = User.objects.all()
    users_profile = Profile.objects.all()

    content = {'title': "specific_applicants",
               'specific_applicants_cards': 5,
               'users_list': users_list,
               'users_profile': users_profile
               }
    return render(request, 'specific_applicants.html', content)

# def marketplace_card(request):
#     content = {'event_details': event_details}
#     return render(request, 'marketplace_card.html', content)


def events(request):
    content = {"title": "events", "events": event_details} 
    return render(request, "users/events.html", content)


# event page
@login_required
def event(request, id, title):

    events = Marketplace.objects.filter(id=id, Speaking_Event_Name=title)
    if not events.exists():
        return redirect("/404")

    if request.method == 'POST':
        Speaker_applied_event = speaker_applied_event()

        if 'Apply' in request.POST:

            if not request.user.is_staff:
                #check if user had fully created a stripe account
                try:
                    stripe_account = Stripe_account.objects.get(user=request.user)
                    stripe_ac_link = (create_login_link(
                        STRIPE_SECRET_KEY, stripe_account.stripe_id))

                except:
                    print("User haven't fully create the account please go to update profile to register the stipe account ")
                    stripe_link = create_account_link(
                    STRIPE_SECRET_KEY, str(stripe_account))
                    print(stripe_link)
                    return redirect(stripe_link)

        
            Speaker_applied_event.user = request.user
            Speaker_applied_event.event = Marketplace.objects.get(id=id, Speaking_Event_Name=title)

            Speaker_applied_event.save()

            try:
                user_group = Group.objects.get(name="speaker")
                user_group.user_set.add(request.user)

            except:
                print("No user group assigned")
        
        elif "see_all_applicants" in request.POST:
            event_id = request.POST.get("see_all_applicants")
            print(event_id)

            return redirect("/payment/accepting_payment2/" + event_id)

        elif "edit" in request.POST:
            event_id = request.POST.get("edit")
            print(event_id)
            return redirect("/edit_event/" + event_id)

        elif 'delete' in request.POST:
            event_id = request.POST.get("delete")
            target_event = Marketplace.objects.get(pk=event_id)
            applied_event = speaker_applied_event.objects.filter(event=target_event, user=request.user)
            applied_event.delete()
            get_event = Marketplace.objects.filter(pk=event_id)
            get_event.delete()
            return redirect("/launch_your_speaking_event/")
                
        elif 'Unapply' in request.POST:
            target_event = Marketplace.objects.get(pk=id)
            applied_events = speaker_applied_event.objects.filter(event=target_event, user=request.user)
            applied_events.delete()



    content = {"event": events.latest("id")}
    return render(request, "event.html", content)

# def jobs(request):
#     content = {"title": "jobs", "jobs": job_details} 
#     return render(request, "users/events.html", content)

@login_required
def job(request, id, title):
    jobs = Job_post.objects.filter(id=id, Job_role=title)
    if not jobs.exists():
        return redirect("/404")

    if seeker_applied_job.objects.filter(user = request.user, job_position = Job_post.objects.get(id=id, Job_role=title)).exists():
        user_applied = True
    else:
        user_applied = False

    if request.method == 'POST':
        Seeker_applied_job = seeker_applied_job()

        if 'Apply' in request.POST:
            Seeker_applied_job.user = request.user
            Seeker_applied_job.job_position = Job_post.objects.get(id=id, Job_role=title)
            Seeker_applied_job.save()
            print("successfully applied")
            user_applied = True

        elif "see_all_applicants" in request.POST:
            job_id = request.POST.get("see_all_applicants")
            print(job_id)

            return redirect("/view_job_applicants/" + job_id)

        elif "edit" in request.POST:
            job_id = request.POST.get("edit")
            print(job_id)
            return redirect("/edit_job/" + job_id)

        elif 'delete' in request.POST:
            job_id = request.POST.get("delete")
            target_job = Job_post.objects.get(pk=job_id)
            applied_job = seeker_applied_job.objects.filter(job_position=target_job, user=request.user)
            applied_job.delete()
            get_job = Job_post.objects.filter(pk=job_id)
            get_job.delete()
            return redirect("/create_jobs")
                
        elif 'Unapply' in request.POST:
            target_job = Job_post.objects.get(pk=id)
            applied_jobs = seeker_applied_job.objects.filter(job_position=target_job, user=request.user)
            applied_jobs.delete()
            user_applied = False

    content = {"job": jobs.latest("id"), "user_applied": user_applied}
    return render(request, "job.html", content)

@login_required
def edit_job(request, id):
    target_job = Job_post.objects.get(pk=id)
    form = JobPost_form(request.POST or None, request.FILES or None, instance=target_job)
    if form.is_valid():
        print("successful")
        form.save()
        return redirect("/create_jobs")
    else:
        print("not successful")
        print(form.errors)
    content = {"job": target_job, "form": form}
    return render(request, "edit_job.html", content)

@login_required
def edit_event(request, id):
    target_event = Marketplace.objects.get(pk=id)
    form = Marketplace_form(request.POST or None, request.FILES or None, instance=target_event)
    if form.is_valid():
        print("successful")
        form.save()
        return redirect("/launch_your_speaking_event/")
    else:
        print("not successful")
        print(form.errors)
    content = {"event": target_event, "form": form}
    return render(request, "edit_event.html", content)