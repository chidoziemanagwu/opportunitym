from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserChangeForm, UserCreationForm)
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Profile, User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email","first_name","last_name",)

    #verify if the email is already registered
    def clean_email(self): 
            email = self.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                raise ValidationError('Email address already registered')
            return email
    #end duplicate email verification

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control Password1', 'id': 'form3Example1c', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control Password2', 'id': 'form3Example1c', 'placeholder': 'Confirm password'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c', 'placeholder': 'Last name'})
            
class CustomLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'id': 'form3Example1c'})

        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-lg'}
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class UserProfileUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = fields = ('first_name', 'last_name')


# class Update_Group_Form(UserChangeForm):
#     group = UserChangeForm.ModelChoiceField(queryset=Group.objects.all(),
#                                             required=True)

#     class Meta(UserChangeForm.Meta):
#         fields = UserChangeForm.Meta.fields + ("group",)
