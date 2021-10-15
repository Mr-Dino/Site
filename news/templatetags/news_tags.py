from django import template
from django.db.models import Count, Q
from news.models import Category, News
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('news', filter=Q(news__is_published=True))).filter(cnt__gt=0)
        cache.set('categories', categories, 60)
    return {'categories': categories}
