from django import template

register = template.Library()

@register.filter
def filter_by_category(news_queryset, category):
    return news_queryset.filter(category=category)
