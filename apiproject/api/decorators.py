from rest_framework.response import Response

def allowed_users(allowed_rolls=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):

            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_rolls:
                return  view_func(request,*args,**kwargs)
            else:
                return Response("Your Role doesnt allow you to access")
        return wrapper_func
    return decorator
