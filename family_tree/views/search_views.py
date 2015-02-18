# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext, loader
from family_tree.models import Person
from django.db.models import Q
import operator
from functools import reduce
from django.core import serializers
from custom_user.decorators import set_language

@login_required
@set_language
def search(request):
    '''
    Shows the search page
    '''

    template = loader.get_template('family_tree/search.html')

    context = RequestContext(request)

    response = template.render(context)
    return HttpResponse(response)



@login_required
@set_language
def get_search_results_json(request):
    '''
    Does the search

    '''
    #break search term into words so they can be any order i.e. Zhang Ziyi can return Ziyi Zhang

    search_words = request.POST.get("search_text").split()

    #http://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list
    #Wow!
    query = reduce(operator.and_, (Q(name__icontains = item) for item in search_words))

    people = Person.objects.filter(family_id = request.user.family_id).filter(query)

    data = serializers.serialize('json', people, fields=('id','name', 'small_thumbnail'))

    return HttpResponse(data, content_type="application/json")
