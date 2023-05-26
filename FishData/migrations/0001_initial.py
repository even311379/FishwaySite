# Generated by Django 3.2.18 on 2023-04-15 15:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CameraInfo',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='監視器名稱')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('frame_rate', models.FloatField(default=30, help_text='單位為fps', verbose_name='影像幀率')),
                ('resolution', models.CharField(choices=[('HD', '1280 x 720'), ('FHD', '1920 x 1080'), ('QHD', '2560 x 1440'), ('UHD', '3840 x 2160')], default='FHD', max_length=100, verbose_name='影像解析度')),
            ],
            options={
                'verbose_name': '監視器資訊',
                'verbose_name_plural': '監視器資訊',
            },
        ),
        migrations.CreateModel(
            name='DetectionModelInfo',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='模型名稱')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '模型資訊',
                'verbose_name_plural': '模型資訊',
            },
        ),
        migrations.CreateModel(
            name='FishAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_time', models.DateTimeField(verbose_name='事件開始時間')),
                ('event_period', models.DurationField(default=datetime.timedelta(seconds=300), verbose_name='事件時段')),
                ('analysis_type', models.CharField(choices=[('DE', '偵測'), ('CO', '計數')], default='DE', max_length=2, verbose_name='分析類型')),
                ('analysis_time', models.DateTimeField(verbose_name='分析時間')),
                ('can_anaylze', models.BooleanField(default=True, help_text='如果水體狀況不佳，則不可分析', verbose_name='是否可分析')),
                ('analysis_log', models.TextField(blank=True, help_text='紀錄分析過程中的特殊狀況', verbose_name='分析紀錄')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FishData.camerainfo', verbose_name='監視器')),
                ('detection_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FishData.detectionmodelinfo', verbose_name='模型')),
            ],
            options={
                'verbose_name': '魚類分析',
                'verbose_name_plural': '魚類分析',
            },
        ),
        migrations.CreateModel(
            name='TargetFishSpecies',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='魚種名稱')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '目標魚種',
                'verbose_name_plural': '目標魚種',
            },
        ),
        migrations.CreateModel(
            name='FishDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='數量')),
                ('frame', models.PositiveIntegerField(default=0, verbose_name='幀數')),
                ('can_detect', models.BooleanField(default=True, help_text='如果水體狀況不佳，則不可偵測', verbose_name='是否可偵測')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fish_detection', to='FishData.fishanalysis', verbose_name='分析')),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FishData.targetfishspecies', verbose_name='魚種')),
            ],
            options={
                'verbose_name': '魚類偵測',
                'verbose_name_plural': '魚類偵測',
            },
        ),
        migrations.CreateModel(
            name='FishCountDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approximate_speed', models.FloatField(default=0, help_text='單位為pixel^2/秒', verbose_name='預估魚類速度')),
                ('approximate_body_length', models.FloatField(default=0, help_text='單位為pixel', verbose_name='預估魚體長度')),
                ('approximate_body_height', models.FloatField(default=0, help_text='單位為pixel', verbose_name='預估魚體高度')),
                ('enter_frame', models.PositiveIntegerField(default=0, verbose_name='進入時幀數')),
                ('leave_frame', models.PositiveIntegerField(default=0, verbose_name='離開時幀數')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fish_count_detail', to='FishData.fishanalysis', verbose_name='分析')),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FishData.targetfishspecies', verbose_name='魚種')),
            ],
            options={
                'verbose_name': '魚類通過數細節',
                'verbose_name_plural': '魚類通過數細節',
            },
        ),
        migrations.CreateModel(
            name='FishCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='通過數')),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fish_count', to='FishData.fishanalysis', verbose_name='分析')),
                ('fish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FishData.targetfishspecies', verbose_name='魚種')),
            ],
            options={
                'verbose_name': '魚類通過數',
                'verbose_name_plural': '魚類通過數',
            },
        ),
    ]