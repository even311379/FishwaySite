

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtailorderable.modeladmin.mixins import OrderableMixin
from .models import *


# Register your models here.

class MenuAdmin(OrderableMixin, ModelAdmin):
    model = Menu
    menu_label = '網頁選單'
    list_display = ('title','position')
    sort_order_field = 'position'

modeladmin_register(MenuAdmin)

