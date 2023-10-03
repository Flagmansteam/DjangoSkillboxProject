from django.views.generic import ListView, DetailView
from .models import *
from django.shortcuts import render
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy

class BasedView(ListView):
    model = Article
    template_name = 'blogapp/artice_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category').prefetch_related('tags').defer('content')

class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
    )


class ArticleDetailView(DetailView):
    model = Article

# настройка rss
class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):    #реализует получение инфо  о статьяъ, которые мы хотим возвращать в списке ленты
        return(
            Article.objects
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:5]  # срез последних пяти статей
        )

    def item_title(self, item: Article):
        return item.title  #возвращаем заголовок

    def item_description(self, item: Article): #возвращаем информацию об объекте, о котором вышла статья
        return item.body[:200]

# метод для генерации ссылки на сайт
    def item_link(self, item: Article):
        return reverse("blogapp:article", kwargs={"pk":item.pk})
