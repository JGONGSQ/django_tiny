from django import forms
from webapp.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib import admin


class PasswordResetForm(forms.Form):

    def is_unique_email(value):
        if User.objects.filter(email=value):
            return True
        else:
            raise ValidationError('There is no account associated with this email address.')

    email = forms.EmailField(label=("Email"), max_length=254, validators=[is_unique_email])

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'server_url': settings.SERVER_NAME,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)

            if html_email_template_name:
                html_email = loader.render_to_string(html_email_template_name, c)
            else:
                html_email = None
            send_mail(subject, email, from_email, [user.email], html_message=html_email)


class UserRegistrationForm(UserCreationForm):

    def validate(value):
        count = 0
        if value.isdigit():
            for digit in value:
                count = count + 1
            if count == 8:
                raise ValidationError('This username is reserved, please choose another one')

    def is_unique_email(value):
        if User.objects.filter(email=value):
            raise ValidationError('This email address has already been registered.')

    username = forms.CharField(min_length=5, required=False, max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Minimum 5 characters, maximum 30 characters'
                                   }
                               ),
                               validators=[validate])

    first_name = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control'
                                 }
                             ),
                             validators=[is_unique_email])
    password1 = forms.CharField(min_length=6, max_length=32,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Minimum 6 characters'}),
                                label='Select a Password')
    password2 = forms.CharField(min_length=6, max_length=32,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Please re-enter your password'}),
                                label='Confirm Password', )
    password1.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    # captcha = CaptchaField()
    # captcha.widget.attrs.update({'class': 'form-control', 'style': 'width: 100%'})

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())