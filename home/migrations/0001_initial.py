# Generated by Django 3.2.18 on 2023-04-08 09:21

from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0083_workflowcontenttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(blank=True, form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('demo', wagtail.blocks.StructBlock([('photo', wagtail.images.blocks.ImageChooserBlock()), ('topic', wagtail.blocks.CharBlock(blank=True)), ('description', wagtail.blocks.RichTextBlock())])), ('gallery', wagtail.blocks.StructBlock([('photo1', wagtail.images.blocks.ImageChooserBlock()), ('photo2', wagtail.images.blocks.ImageChooserBlock()), ('photo_big', wagtail.images.blocks.ImageChooserBlock())])), ('dashboard', wagtail.blocks.CharBlock(blank=True, helper_text='dash app', max_length=50))], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]