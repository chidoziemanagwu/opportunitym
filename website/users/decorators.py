from django.http import HttpResponse
from django.shortcuts import redirect

#redirects already logged in user to homepage
def unauthenticated_user (view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper

#allows permission to groups
def allowed_users(allowed_groups = []):
    def decorator(view_func):
        def wrapper (request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_groups:
                return view_func (request, *args, **kwargs)
            else:
                return HttpResponse("You are are not authorized")
        return wrapper
    return decorator