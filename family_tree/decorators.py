from family_tree.models import Person
from django.shortcuts import get_object_or_404
from functools import wraps
from django.http import Http404

def same_family_required(func):
    '''
    Decorator to automatically load a person and check if the user is allowed to see them
    Passes the person object into the parent function to reduce number of db calls
    Also sets language
    '''
    @wraps(func)
    def inner(request, person_id = 0, person = None, *args, **kwargs):

        if person_id == 0:
            person = get_object_or_404(Person, user_id = request.user.id)
        else:
            person = get_object_or_404(Person, id = person_id)

        if request.user.family_id != person.family_id:
            raise Http404


        return func(request=request, person_id=person_id, person=person, *args, **kwargs)


    return inner