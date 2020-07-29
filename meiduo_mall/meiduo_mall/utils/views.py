from django.http import JsonResponse


# 定义一个过滤的闭包:
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        # 过滤是否登录:
        if request.user.is_authenticated:
            # 登录:
            return func(request, *args, **kwargs)
        else:
            # 没有登录:
            return JsonResponse({'code':400,
                                 'errmsg':"未登录, 请赶紧登录"})
    return wrapper


# 定义一个能够过滤是否登录的Mixin扩展类:
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator(view)
        return view

