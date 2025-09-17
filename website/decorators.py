from django.shortcuts import redirect
from django.contrib import messages


def login_required_restrictive(view):
    """
    decorator for views that checks that the user is logged in
    if the user is not logged in, he will be redirected and the request won't be saved
    """
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect('/404')
        return view(request)

    return wrapper


def ajax_request_required(view):
    """
    decorator for views that checks that the request includes headers of an Ajax request 
    """
    def wrapper(request, *args, **kwargs):
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return redirect('/404')
        return view(request, *args, **kwargs)

    return wrapper


def country_required(view):
    """
    decorator for views that checks that the user has a country selected
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.user_profile.country:
            messages.error(
                request, "The page you are trying to access requires to have a country selected")
            return redirect('/404')

        return view(request, *args, **kwargs)

    return wrapper
