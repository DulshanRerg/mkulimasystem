from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=None):
    """
    Decorator for views that checks whether the logged-in user has one of the allowed roles.
    
    Args:
        allowed_roles (list): A list of roles that are allowed to access the view.
        
    Raises:
        PermissionDenied: If the user's role is not in the allowed roles.
    """
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                raise PermissionDenied("You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
