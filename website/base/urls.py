from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('subscribe_to_newsletter', views.subscribe_to_newsletter, name="subscribe_to_newsletter"),
    path('unsubscribe_to_newsletter/<int:email_id>', views.unsubscribe_to_newsletter, name="unsubscribe_to_newsletter"),
    path('add_opportunity', views.add_opportunity, name="add_opportunity"),
    path('submit_interest_for_opp_portfolio', views.submit_interest_for_opp_portfolio, name="submit_interest_for_opp_portfolio"),
    path('submit_interest_for_opp_verified', views.submit_interest_for_opp_verified, name="submit_interest_for_opp_verified"),
    path('find_jobs', views.find_jobs, name="find_jobs"),
    path('create_jobs', views.create_jobs, name="create_jobs"),
    path('view_job_applicants/<int:job_id>/', views.view_job_applicants, name="view_job_applicants"),
    path('test/', views.test, name="test"),
    path('launch_your_speaking_event/', views.launch_your_speaking_event,
         name="launch_your_speaking_event"),
    path('about/', views.about, name="about"),
    path('opportunity_board/', views.opportunity_board, name="opportunity_board"),
    path('get_in_touch/', views.get_in_touch, name="get_in_touch"),
    path('speakers/', views.speakers, name="speakers"),
    path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
    path('terms_and_conditions/', views.terms_and_conditions,
         name="terms_and_conditions"),
    #     path('register/', views.register, name='register')
    path('404/', views.error404, name='404'),
    path('cookies/', views.cookie_statement, name='cookies'),
    path('contact_us/', views.contact_us, name='contact_us'),
    # path('profile/', views.profile, name='Your profile'),
    path('specific_applicants/<str:event_id>', views.specific_applicants, name='specific_applicants'),
    #     path('marketplace/', views.marketplace, name='marketplace'),
    path("events", views.events, name="events"),
    path("events/<int:id>/<str:title>", views.event, name="event_detail"),
    path("jobs/<int:id>/<str:title>", views.job, name="job_detail"),
    path("edit_job/<int:id>", views.edit_job, name="edit_job"),
    path("edit_event/<int:id>", views.edit_event, name="edit_event"),
    path('new', views.new, name="new"),
    path('book_oliver', views.book_oliver, name="book_oliver"),
    path('coming_soon/', views.coming_soon, name="coming_soon"),
    path('news/', views.news_page, name="news"),
    path('news/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('modify/<slug:post_slug>/', views.modify_post, name='modify_post'),
    path('my_post/', views.my_post, name='my_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
