from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock


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
        ('gallery', blocks.ListBlock(ImageChooserBlock())),        
        ('dashboard', blocks.CharBlock(blank=True, max_length=50, helper_text="dash app"))               
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

