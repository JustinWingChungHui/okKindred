from family_tree.models import Person
from django.shortcuts import get_object_or_404
from django.http import Http404
from functools import wraps

def same_family_required(func):
    '''
    Decorator to automatically load a person and check if the user is allowed to see them
    Passes the person object into the parent function to reduce number of db calls
    '''
    @wraps(func)
    def inner(request, person_id = 0, person = None, *args, **kwargs):

        if person_id == 0:
            person = get_object_or_404(Person, user_id = request.user.id)
        else:
            person = get_object_or_404(Person, id = person_id)

        if request.user.family_id == person.family_id:
            return func(request=request, person_id=person_id, person=person, *args, **kwargs)
        else:
            raise Http404

    return inner