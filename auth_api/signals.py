from django.core.mail import send_mail
from django.dispatch import receiver
from axes.signals import user_locked_out


@receiver(user_locked_out)
def handle_user_locked_out(sender, request, username, ip_address, **kwargs):

    subject = "ok!Kindred Account Locked Notification"

    content = """
        IP Address: {0} blocked for too many failed login attempts

        Username: {1}

        Request Metadata:
        {2}

        Request Headers:
        {3}
        """.format(ip_address, username, request.META, request.headers)

    send_mail(
        subject,
        content,
        'info@okkindred.com',
        ['info@okkindred.com'],
        fail_silently=False)