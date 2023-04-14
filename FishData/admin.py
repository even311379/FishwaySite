from django.contrib import admin

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from .models import *

from .wagtail_hooks import ExportModelAdminMixin

# Register your models here.

class TargetFishSpeciesAdmin(ModelAdmin):
    model = TargetFishSpecies
    menu_label = '目標魚種'
    list_display = ('name',)

class CameraInfoAdmin(ModelAdmin):
    model = CameraInfo
    menu_label = '監視器資訊'
    list_display = ('name', 'frame_rate', 'resolution',)

class DetectionModelInfoAdmin(ModelAdmin):
    model = DetectionModelInfo
    menu_label = '模型資訊'
    list_display = ('name',)

class FishAnalysisAdmin(ModelAdmin):
    model = FishAnalysis
    menu_label = '魚類分析' 
    list_display = ('camera', 'detection_model', 'event_time', 'event_period', 'analysis_type', 'analysis_time', 'can_anaylze',)
    list_filter = ('camera', 'detection_model', 'event_time', 'analysis_type', 'analysis_time', 'can_anaylze',)
        

class FishCountAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "FishData/export_csv.html"
    model = FishCount
    menu_label = '魚類通過數'
    list_display = ('analysis', 'fish', 'count')
    list_filter = ('analysis__camera', 'analysis__detection_model', 'analysis__event_time', 'fish', 'count')

class FishCountDetailAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "FishData/export_csv.html"
    model = FishCountDetail
    menu_label = '魚類通過細節'
    list_display = ('analysis', 'fish', 'approximate_speed', 'approximate_body_length', 'approximate_body_height','enter_frame', 'leave_frame',)
    list_filter = ('analysis__camera', 'analysis__detection_model', 'analysis__event_time', 'fish', 'approximate_speed', 'approximate_body_length', 
                   'approximate_body_height', 'enter_frame', 'leave_frame',)

class FishDetectionAdmin(ExportModelAdminMixin, ModelAdmin):
    index_template_name = "FishData/export_csv.html"
    model = FishDetection
    menu_label = '魚類偵測'
    list_display = ('analysis', 'fish', 'count', 'frame', 'can_detect',)
    list_filter = ('analysis__camera', 'analysis__detection_model', 'analysis__event_time', 'fish', 'count', 'frame', 'can_detect',)

        
class DataGroup(ModelAdminGroup):
    menu_label = '魚道監測資料'
    menu_icon = 'warning'
    items = (TargetFishSpeciesAdmin, CameraInfoAdmin, DetectionModelInfoAdmin, FishAnalysisAdmin, FishCountAdmin, FishCountDetailAdmin, FishDetectionAdmin)

modeladmin_register(DataGroup)