# Generated by Django 3.2.18 on 2023-04-17 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FishData', '0003_alter_fishanalysis_analysis_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fishanalysis',
            old_name='can_anaylze',
            new_name='can_analyze',
        ),
    ]
