from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import *


class PostAdminForm(forms.ModelForm):
	body = forms.CharField(widget=CKEditorUploadingWidget())

	class Meta:
		model = Post
		fields = '__all__'


class PostAdmin(admin.ModelAdmin):
	form = PostAdminForm

class OpportunitySuggestionAdmin(admin.ModelAdmin):
    list_display= ('opportunity', 'count')

class OpportunitySuggestionUserDataAdmin(admin.ModelAdmin):
    list_display= ('user_id', 'firstname', 'email', 'telephone', 'opportunity', 'timestamp', 'desired_region', 'country', 'countrycode', 'city')

admin.site.register(Marketplace)
admin.site.register(speaker_applied_event)
admin.site.register(seeker_applied_job)
admin.site.register(Post, PostAdmin)
admin.site.register(Events_topic) #event topic list admin panel
admin.site.register(TeamMember)
admin.site.register(Opportunity_suggestion, OpportunitySuggestionAdmin)
admin.site.register(Opportunity_suggestion_user_data, OpportunitySuggestionUserDataAdmin)
admin.site.register(Newsletter_email)
admin.site.register(Opportunity_Portfolio_mailing_list)
admin.site.register(Opportunity_Verified_mailing_list)
admin.site.register(Job_post)

# @admin.register(User)
# class UserAdmin(User):
#     fields = ('full_name', 'email', 'password')
#     list_display = ['id', 'full_name', 'email', 'password']


# @admin.register(Speaker)
# class SpeakerAdmin(admin.ModelAdmin):
#     fields = ('User', 'Name', 'Description', 'Email', 'Updated', 'Created')
#     list_display = ['id', 'User', 'Name',
#                     'Description', 'Email', 'Updated', 'Created']


# @admin.register(Topic)
# class TopicAdmin(admin.ModelAdmin):
#     fields = ('Topic', 'Description', 'Updated', 'Created')
#     list_display = ['id', 'Topic', 'Description', 'Updated', 'Created']


# @admin.register(Event)
# class TopicAdmin(admin.ModelAdmin):
#     fields = ('Topic_name', 'Speaker_name', 'Created_by', 'Name',
#               'Description', 'DateTime', 'Location', 'Guest_Capacity', 'Status')
#     list_display = ['id', 'Topic_name', 'Created_by', 'Name', 'DateTime']
