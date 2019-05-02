from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation

from axes.handlers.proxy import AxesProxyHandler
from django.contrib.auth.signals import user_login_failed

from custom_user.models import User
from family_tree.models import Person
from sign_up.models import SignUp

from common.utils import intTryParse


def sign_up(request):
    '''
    Shows the sign up form
    '''
    # Do not allow logged in users to create another account
    if request.user.is_authenticated:
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

    # assign non required stuff
    birth_year, birth_year_valid = intTryParse(request.POST.get("birth_year"))
    if not birth_year_valid:
        birth_year = 0

    address = request.POST.get("address")
    if not address:
        address = ""

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
                        language = language,
                        address = address,
                        birth_year = birth_year)

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

    if SignUp.objects.filter(email_address = email).count():
        return True

    return False

def sign_up_confirmation(request, confirmation_key):
    '''
    Handles the sign up confirmation
    '''
    #Check ip has not been locked
    if not AxesProxyHandler.is_allowed(request):
        raise Http404

    try:
        sign_up = SignUp.objects.get(confirmation_key=confirmation_key)
    except:

        user_login_failed.send(
                            sender=sign_up_confirmation,
                            credentials={'username': confirmation_key },
                            request=request)
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
    user = auth.authenticate(username=user.email, password=password, request=request)
    auth.login(request, user)

    return HttpResponseRedirect('/home/')

