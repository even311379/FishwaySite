from django.db import models
from django_extensions.db.fields import AutoSlugField

from wagtail.models import Page
from wagtailorderable.models import Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting
)
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel


class CommonPage(Page):
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", blank=True)),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('demo', blocks.StructBlock([
           ('iframe', blocks.URLBlock(blank=True, max_length=100, help_text="iframe url", required=False)),
           ('photo', ImageChooserBlock(required=False)),
           ('topic', blocks.CharBlock(blank=True)),
           ('description', blocks.RichTextBlock()),
        ], help_text="Use either iframe or photo")),
        ('gallery', blocks.ListBlock(ImageChooserBlock(), help_text="This is designed for **2 to 6** images")),        
        ('dashboard', blocks.CharBlock(blank=True, max_length=50, helper_text="dash app"))               
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

class MenuItem(Orderable):
    link_page = models.ForeignKey(CommonPage, blank=True, null=True, on_delete=models.SET_NULL)
    menu = ParentalKey("Menu", related_name='menu_items')

    content_panels = [FieldPanel('title'), PageChooserPanel(link_page)]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        return '#'


class Menu(ClusterableModel, Orderable):
    title = models.CharField(max_length=50)
    position = models.IntegerField(null=False, blank=True, default=0, editable=False)

    panels = [
        MultiFieldPanel([
            FieldPanel("title")
        ], heading="Menu"),
        InlinePanel("menu_items", label="Menu Item")
    ]

    def __str__(self):
        return self.title

@register_setting(icon='placeholder')
class GenericPageContent(BaseGenericSetting):
    banner_bg_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, help_text="頁首底圖", blank=True)
    banner_bg_tint = ColorField(blank=True, help_text="頁首色調")
    # footer_bg_image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', null=True, help_text="頁首底圖", blank=True)
    # footer_bg_tint = ColorField(blank=True, help_text="頁尾色調")
    # copyright_info = models.CharField(max_length=100, blank=True)
    
    class Meta:
        verbose_name = "頁首與頁尾"
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel('banner_bg_image'),
                NativeColorPanel("banner_bg_tint"),
            ],
            "頁面旗幟(Banner)"),
        # MultiFieldPanel(
        #     [
        #         FieldPanel('footer_bg_image'),
        #         FieldPanel("copyright_info"),
        #         NativeColorPanel("footer_bg_tint"),
        #     ],
        #     '頁尾')
    ]