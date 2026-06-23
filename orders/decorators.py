from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from accounts.models import User

def role_required(roles:list):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login_url') # Replace with your login URL name
            
            if request.user.role not in roles:
                raise PermissionDenied("Access denied.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# def station_required(stations):
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs):
#           if request.user.role != User.ROLE_CHOICES.KITCHEN:
#                 raise PermissionDenied

#           if request.user.kitchen_station not in stations:
#                 raise PermissionDenied
#           return view_func(request, *args, **kwargs)
            
#         return wrapper
#     return decorator