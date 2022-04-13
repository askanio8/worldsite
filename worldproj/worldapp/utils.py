from .models import *


menu = [{'title': "About", 'url_name': 'about'},
        {'title': "Add town", 'url_name': 'addtown'},
        {'title': "Contact", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 50  # в шаблон будут переданы paginator и page_obj

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            context['menu'] = menu
        else:
            user_menu = menu.copy()
            user_menu.pop(1)
            context['menu'] = user_menu
        return context
