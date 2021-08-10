from django.views import View


class CustomView(View):
    def dispatch(self, request, *args, **kwargs):
        if 'delete' in request.POST.keys():
            handler = getattr(self, 'delete', self.http_method_not_allowed)
            return handler(request, *args, **kwargs)
        return super().dispatch(request)
