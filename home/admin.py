from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtailorderable.modeladmin.mixins import OrderableMixin
from .models import *


# Register your models here.


class MenuAdmin(OrderableMixin, SnippetViewSet):
    model = Menu
    menu_label = "網頁選單"
    list_display = ("title", "position")
    sort_order_field = "position"


register_snippet(MenuAdmin)
