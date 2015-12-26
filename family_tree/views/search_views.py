# encoding: utf-8
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from functools import reduce

from family_tree.models import Person
from custom_user.decorators import set_language

import operator

@login_required
@set_language
def search(request):
    '''
    Shows the search page
    '''
    return render(request, 'family_tree/search.html')



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
