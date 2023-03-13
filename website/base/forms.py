from dataclasses import field

from django.forms import ModelForm, CharField, TextInput, Textarea
from ckeditor_uploader.widgets import CKEditorUploadingWidget


from .models import *

# class RegisterForm(ModelForm):
#     class Meta:
#         model = User
#         fields = "__all__"


# class Speaker_Register_Form(ModelForm):
#     class Meta:
#         model = Speaker
#         filter-'__all__'

class Marketplace_form(ModelForm):
    Description = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Marketplace
        fields = "__all__"

    def clean(self):
        cd = self.cleaned_data
        if cd.get('date').date() < timezone.now().date():
            self._errors['date'] = self.error_class(['Date cannot be in the past'])
            del cd['date']
        return cd

    def __init__(self, *args, **kwargs):
        super(Marketplace_form, self).__init__(*args, **kwargs)
        self.fields['Creator'].widget.attrs.update(
            {'class': 'form-control d-none', 'id': 'form3Example1c'})
        self.fields['Image_URL'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c'})
        self.fields['Speaking_Event_Name'].widget.attrs.update(
            {'class': 'form-control Password1', 'id': 'form3Example1c', 'placeholder': 'Title'})
        self.fields['Type'].widget.attrs.update(
            {'class': 'form-control Password2', 'id': 'form3Example1c'})
        self.fields['Location'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Location'})
        self.fields['Capacity'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Capacity'})
        self.fields['Topic'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c'})
        self.fields['Worth'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Worth'})
        self.fields['date'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'YYYY-MM-DD HH:MM:SS'})
        self.fields['Description'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Description'})
        self.fields['Status'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Status'})

class JobPost_form(ModelForm):
    Description = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Job_post
        fields = "__all__"

    def clean(self):
        cd = self.cleaned_data
        if cd.get('Deadline').date() < timezone.now().date():
            self._errors['Deadline'] = self.error_class(['Date cannot be in the past'])
            del cd['Deadline']
        return cd

    def __init__(self, *args, **kwargs):
        super(JobPost_form, self).__init__(*args, **kwargs)
        self.fields['Creator'].widget.attrs.update(
            {'class': 'form-control d-none', 'id': 'form3Example1c'})
        self.fields['Image_URL'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c'})
        self.fields['Email'].widget.attrs.update(
            {'class': 'form-control Password1', 'id': 'form3Example1c', 'placeholder': 'Email'})
        self.fields['Job_role'].widget.attrs.update(
            {'class': 'form-control Password2', 'id': 'form3Example1c', 'placeholder': 'Job role'})
        self.fields['Company'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Company'})
        self.fields['Job_mode'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Job mode'})
        self.fields['Status'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Status'})
        self.fields['Deadline'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'YYYY-MM-DD HH:MM:SS'})
        self.fields['Salary'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Salary'})
        self.fields['Description'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Description'})

class PostForm(ModelForm):
    body = CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        exclude = ('author',)

# class OpportunityForm(ModelForm):
#     opportunity = TextInput
#     class Meta:
#         model = Opportunity_suggestion
#         fields = ['opportunity']