from django import template

register = template.Library()


@register.filter
def filter_by(new_queryset, argument):
    argument = "".join(argument).split(",")
    d = {
        argument[0]: argument[1]
    }
    return new_queryset.filter(**d)[:int(argument[2])]



