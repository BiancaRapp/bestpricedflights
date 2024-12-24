from django import template

register = template.Library()


@register.filter
def pk(queryset, pk):
    return queryset.filter(pk=pk).first()
