from django.shortcuts import render


def handler404(request, *args, **argv):
    '''
    Custom 404 handler
    '''
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler505(request, *args, **argv):
    '''
    Custom 505 handler
    '''
    response = render(request, '505.html', {})
    response.status_code = 505
    return response