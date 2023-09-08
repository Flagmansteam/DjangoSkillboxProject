from django.views.generic import ListView
from .models import *


class BasedView(ListView):
    model = Article
    template_name = 'blogapp/artice_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').prefetch_related('tags').defer('content')
