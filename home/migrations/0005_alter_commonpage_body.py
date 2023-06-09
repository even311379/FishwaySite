# Generated by Django 3.2.18 on 2023-04-10 06:16

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_commonpage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commonpage',
            name='body',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(blank=True, form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('demo', wagtail.blocks.StructBlock([('iframe', wagtail.blocks.CharBlock(blank=True, help_text='iframe url', max_length=100, required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('topic', wagtail.blocks.CharBlock(blank=True)), ('description', wagtail.blocks.RichTextBlock())], collapsed=False, collapsible=True, help_text='Use either iframe or photo')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock())), ('dashboard', wagtail.blocks.CharBlock(blank=True, helper_text='dash app', max_length=50))], blank=True, use_json_field=True),
        ),
    ]
