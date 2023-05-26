from django.db import models
from django_extensions.db.fields import AutoSlugField

from wagtail.models import Page
from wagtailorderable.models import Orderable
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel




class CommonPage(Page):
    
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title", blank=True)),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('demo', blocks.StructBlock([
           ('iframe', blocks.CharBlock(blank=True, max_length=100, help_text="iframe url", required=False)),
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
