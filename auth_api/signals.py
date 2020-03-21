from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import get_template
from django.utils import translation

from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset

from axes.signals import user_locked_out

@receiver(user_locked_out)
def handle_user_locked_out(sender, request, username, ip_address, **kwargs):

    subject = "ok!Kindred Account Locked Notification"

    body = request.data

    if body and 'password' in body:
        body['password'] = '#######'

    content = """
        IP Address: {0} blocked for too many failed login attempts

        body: {1}

        Request Metadata:
        {2}

        Request Headers:
        {3}
        """.format(ip_address, body, request.META, request.headers)

    send_mail(
        subject,
        content,
        'info@okkindred.com',
        ['info@okkindred.com'],
        fail_silently=False)



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    language = reset_password_token.user.language

    translation.activate(language)

    subject = translation.ugettext('ok!Kindred Password Reset')

    content = get_template('auth_api/password_reset_plain.html').render(
                {
                    'language': language,
                    'reset_password_token' : reset_password_token.key,
                    'domain' : settings.DOMAIN
                })

    content_html = get_template('auth_api/password_reset.html').render(
                {
                    'language': language,
                    'reset_password_token' : reset_password_token.key,
                    'domain' : settings.DOMAIN
                })

    send_mail(
        subject,
        content,
        'info@okkindred.com',
        [reset_password_token.user.email],
        fail_silently=False,
        html_message=content_html)



@receiver(post_password_reset)
def post_password_reset(user, *args, **kwargs):
    """
    Called once user has changed password.  Sends email to confirm change
    """
    language = user.language

    translation.activate(language)

    subject = translation.ugettext('ok!Kindred Password Successfully Updated')

    content = get_template('auth_api/password_changed_plain.html').render(
                {
                    'language': language,
                    'domain' : settings.DOMAIN
                })

    content_html = get_template('auth_api/password_changed.html').render(
                {
                    'language': language,
                    'domain' : settings.DOMAIN
                })

    send_mail(
        subject,
        content,
        'info@okkindred.com',
        [user.email],
        fail_silently=False,
        html_message=content_html)
