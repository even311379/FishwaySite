from django import template
from ..models import Menu, MenuItem

register = template.Library()

@register.simple_tag()
def get_menus():
    return Menu.objects.all().order_by('position')