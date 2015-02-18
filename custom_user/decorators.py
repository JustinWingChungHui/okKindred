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