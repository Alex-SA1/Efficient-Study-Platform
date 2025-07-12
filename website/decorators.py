from django.shortcuts import redirect


def login_required_restrictive(view):
    """
    decorator for views that checks that the user is logged in
    if the user is not logged in, he will be redirected and the request won't be saved
    """
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect('/error_404')
        return view(request)

    return wrapper


def ajax_request_required(view):
    """
    decorator for views that checks that the request includes headers of an Ajax request 
    """
    def wrapper(request):
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return redirect('/error_404')
        return view(request)

    return wrapper
