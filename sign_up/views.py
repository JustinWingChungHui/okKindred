from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

from axes.decorators import is_already_locked, get_ip, check_request
from axes.models import AccessLog

from custom_user.models import User
from family_tree.models import Person
from sign_up.models import SignUp


def sign_up(request):
    '''
    Shows the sign up form
    '''
    # Do not allow logged in users to create another account
    if request.user.is_authenticated():
        raise Http404

    if request.method == 'POST':
        return sign_up_post(request)

    return render(request, 'sign_up/sign_up.html', {
                                'languages' : settings.LANGUAGES,
                            })


def sign_up_post(request):
    '''
    Handles when a sign up is submitted
    '''
    name = request.POST.get("name").strip()
    email = request.POST.get("email").strip().lower()
    gender = request.POST.get("gender")
    language = request.POST.get("language")

    try:
        validate_email(email)
    except ValidationError:
        # return invalid email template
        return render(request, 'sign_up/invalid_email.html')

    #Check email is not being used
    if is_email_in_use(email):
        return render(request, 'sign_up/email_in_use.html')

    new_signup = SignUp.objects.create(
                        name = name,
                        email_address = email,
                        gender = gender,
                        language = language)

    translation.activate(language)

    return render(request, 'sign_up/check_email.html', {
                                'new_signup' : new_signup,
                            })


def is_email_in_use(email):
    '''
    Checks if email is in use
    '''
    if User.objects.filter(email = email).count():
        return True

    if Person.objects.filter(email = email).count():
        return True

    return False

def sign_up_confirmation(request, confirmation_key):
    '''
    Handles the sign up confirmation
    '''
    #Check ip has not been locked
    if is_already_locked(request):
        raise Http404

    try:
        sign_up = SignUp.objects.get(confirmation_key=confirmation_key)
    except:
        #Log access attempt
        AccessLog.objects.create(
                         user_agent=request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
                         ip_address=get_ip(request),
                         username=confirmation_key,
                         http_accept=request.META.get('HTTP_ACCEPT', '<unknown>'),
                         path_info=request.META.get('PATH_INFO', '<unknown>'),
                         trusted=False,
                         )


        check_request(request, True)
        raise Http404

    if request.method == 'POST':
        return sign_up_confirmation_post(request, sign_up)

    translation.activate(sign_up.language)

    return render(request, 'sign_up/choose_password.html', {
                                'confirmation_key' : confirmation_key,
                            })


def sign_up_confirmation_post(request, sign_up):
    '''
    Handles the sign up confirmation post request
    '''
    password = request.POST.get("password")

    #Invalid password should be checked bu UI
    if len(password) < 8:
        raise Http404

    user = sign_up.complete_registration(password)
    user = auth.authenticate(username=user.email, password=password)
    auth.login(request, user)

    return HttpResponseRedirect('/home/')

