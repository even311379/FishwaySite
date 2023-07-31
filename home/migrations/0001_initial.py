# Generated by Django 4.2.3 on 2023-07-29 16:12

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
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
            name='CommonPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(blank=True, form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('demo', wagtail.blocks.StructBlock([('iframe', wagtail.blocks.CharBlock(blank=True, help_text='iframe url', max_length=100, required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('topic', wagtail.blocks.CharBlock(blank=True)), ('description', wagtail.blocks.RichTextBlock())], help_text='Use either iframe or photo')), ('gallery', wagtail.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(), help_text='This is designed for **2 to 6** images')), ('dashboard', wagtail.blocks.CharBlock(blank=True, helper_text='dash app', max_length=50))], blank=True, use_json_field=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('title', models.CharField(max_length=50)),
                ('position', models.IntegerField(blank=True, default=0, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.commonpage')),
                ('menu', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_items', to='home.menu')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
