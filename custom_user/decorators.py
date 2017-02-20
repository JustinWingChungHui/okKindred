from django.utils import translation
from functools import wraps

def set_language(func):
    '''
    Decorator to set the language
    '''
    @wraps(func)
    def inner(request, *args, **kwargs):

        if request.user:
            translation.activate(request.user.language)
            request.session[translation.LANGUAGE_SESSION_KEY] = request.user.language

        return func(request=request, *args, **kwargs)


    return inner


def set_pythonanywhere_external_ip(func):
    '''
    Ensures that the external IP address is set not the PythonAnywhee load balancer
    '''
    @wraps(func)
    def inner(request, *args, **kwargs):
        request.META['REMOTE_ADDR'] = request.META.get('HTTP_X_REAL_IP')

        return func(request=request, *args, **kwargs)

    return inner