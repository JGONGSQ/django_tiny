import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib import messages
# from webapp.utils import is_eight_digit
# from webapp.utils_email import REGISTRATION_COMPLETE_EMAIL, send_alternate_email_confirmation
# from webapp.forms import PasswordChangeForm, UserRegistrationForm
from webapp.models import UserPermissionType

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
# from suds.client import Client
from django.views.decorators.csrf import csrf_exempt


@cache_control(no_cache=True, must_revalidate=True)
def webapp_login(request):
    c = {}
    c.update(csrf(request))

    if request.POST:
        c.update(csrf(request))
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        # if user is not none at this point, log in
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user:user_home'))
            else:
                messages.error(request, 'This account has been disabled. Please contact support if you believe this to be a mistake.')
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.error(request, 'Login failed. Please check your credentials and try again.')
            return HttpResponseRedirect(reverse('auth:login'))

    else:
        if request.user.is_authenticated():
            if 'next' in request.POST:
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            if 'next' in request.GET:
                return render(request, 'webapp/registration/login.html', {'next': request.GET['next']})
            else:
                return render(request, 'webapp/registration/login.html')


def webapp_logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # create new user account
            # new_user = form.save()


            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password1')

            new_user = User.objects.create_user(
                username=email[:30], # limit to 30 chars to fit within django's default username field
                email=email,
                password=password,
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize(),
            )
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'

            profile = UserPermissionType.objects.create(user=new_user, type=UserPermissionType.USER_TYPE_STUDENT,
                                                        university=UserPermissionType.UNIVERSITY_TYPE_DEFAULT)

            login(request, new_user)

            msg = "Registration complete. Welcome " + profile.user.first_name + " " + profile.user.last_name
            messages.success(request, msg)

            send_mail(
                'Forrest New User Registration',
                REGISTRATION_COMPLETE_EMAIL.format(username=new_user.username),
                settings.NO_REPLY,
                [new_user.email],
            )

            return HttpResponseRedirect(reverse('home'))

        else:
            return render(request, 'webapp/registration/registration.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'webapp/registration/registration.html', {'form': form})


# #checks if a user is trying to a pheme account password
@csrf_exempt
def pheme_password_reset(request):
    if request.POST:
        email = request.POST.get('email')
        data = {}
        try:
            user = User.objects.get(email=email)
            if is_eight_digit(user.username):
                data['message'] = 'Please reset your password on the <a href="https://www.pheme.uwa.edu.au/">Pheme</a> website.'
                data['response'] = 'failure'
            else:
                data['response'] = 'success'

        except User.DoesNotExist:
            data['message'] = 'A user with this email address was not found.'
            data['response'] = 'failure'

        return HttpResponse(json.dumps(data), content_type="application/json")


def is_number(s):
    """
       Check if the string is likely to be a student/staff number
    :param s: username
    :return: True if numeric
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def email_is_valid(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


@login_required
def password_change(request):
    c = {'form': PasswordChangeForm()}
    return render(request, 'webapp/registration/password_change_form.html', c)


@login_required
def password_change_done(request):

    c = {}
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)

        if form.is_valid():
            user = request.user

            if (user.check_password(request.POST['current_password'])):
                if (request.POST['new_password'] == request.POST['confirm_password']):
                    user.set_password(request.POST['new_password'])
                    user.save()
                    c['message']= "Your password has been successfully changed"
                    return render(request, 'webapp/registration/password_change_done.html', c)
                else:
                    c['form'] = PasswordChangeForm()
                    c['message'] = "New passwords do not match"
            else:
                c['form'] = PasswordChangeForm()
                c['message'] = "Password incorrect. Please check that you have typed your old password correctly"

        else:
            c['form'] = PasswordChangeForm()
            c['message'] = "All fields are required"

        return render(request, 'webapp/registration/password_change_form.html', c)
    else:
        c['form'] = PasswordChangeForm()
        return render(request, 'webapp/registration/password_change_form.html', c)




