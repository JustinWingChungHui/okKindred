from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from axes.decorators import is_already_locked, check_request
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from custom_user.decorators import set_language
from family_tree.models import Person

'''
Authentication views based on https://www.youtube.com/watch?v=CFypO_LNmcc
'''

def login(request):
    '''
    Handles login requests
    '''

    c = { 'next': request.GET.get('next', '') }
    c.update(csrf(request))

    return render( request, 'custom_user/login.html', c)


def auth_view(request):
    '''
    Handles the authentication from the login screen
    '''
    if is_already_locked(request):
        return account_locked(request)

    username = request.POST.get('username', '').lower()
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    login_unsuccessful = user is None

    check_request(request, login_unsuccessful)


    if login_unsuccessful:
        return HttpResponseRedirect('/accounts/invalid')

    target_url = request.POST.get('next', '/')

    auth.login(request, user)
    return HttpResponseRedirect(target_url)





def logged_in(request):
    return render(request, 'custom_user/logged_in.html',
                                {'username': request.user.username})

def invalid_login(request):
    return render(request, 'custom_user/invalid_login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def account_locked(request):
    return render(request, 'custom_user/account_locked.html')

@login_required
@set_language
def settings_view(request):
    '''
    Shows the settings view
    '''

    return render(request, 'custom_user/settings.html', {
                                'user' : request.user,
                                'languages' : settings.LANGUAGES,
                            })

@login_required
def change_password_post(request):
    '''
    Handles the password change
    '''
    new_password = request.POST.get("password")

    #Invalid password
    if len(new_password) < 8:
        return HttpResponseRedirect('/settings/')

    request.user.set_password(new_password)
    request.user.save()

    return HttpResponseRedirect('/')


@login_required
def update_user_setting_post(request):
    '''
    Handles the update of individual user settings
    '''

    try:
        field_name = request.POST.get("name")

        if field_name in ['receive_update_emails','language','receive_photo_update_emails']:

            setattr(request.user, field_name, request.POST.get("value"))
            request.user.save()
            return HttpResponse(status=200, content="OK")

        return HttpResponse(status=405, content=_('Access denied'))

    except Exception as e:
        return HttpResponse(status=405, content=e)


@login_required
def delete_account_post(request):

    try:
        delete_profile = (request.POST.get("delete_profile") == '1')

        #Delete the profile
        try:
            person = Person.objects.get(user_id=request.user.id)

            if delete_profile:
                person.delete()
            else:
                person.user_id = None
                person.email_address = None
                person.save()

        except:
            pass

        #Delete the user
        request.user.delete()

        return HttpResponseRedirect('/')

    except Exception as e:
        return HttpResponse(status=405, content=e)