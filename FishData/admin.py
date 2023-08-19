from django.contrib import admin

# from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import *

from .wagtail_hooks import ExportModelAdminMixin

# Register your models here.


class TargetFishSpeciesAdmin(SnippetViewSet):
    model = TargetFishSpecies
    menu_label = "目標魚種"
    list_display = ("name",)


class CameraInfoAdmin(SnippetViewSet):
    model = CameraInfo
    menu_label = "監視器資訊"
    list_display = ("name",)


class DetectionModelInfoAdmin(SnippetViewSet):
    model = DetectionModelInfo
    menu_label = "模型資訊"
    list_display = ("name",)


class FishwayUtilityAnalysisAdmin(SnippetViewSet):
    model = FishwayUtilityAnalysis
    menu_label = "魚道使用狀況分析"
    list_display = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "detection_frequency",
    )
    list_filter = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "detection_frequency",
    )


class FishwayPassAnalysisAdmin(SnippetViewSet):
    model = FishwayPassAnalysis
    menu_label = "魚道通過分析"
    list_display = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "sample_length",
    )
    list_filter = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "sample_length",
    )


class FishwayUtilityAdmin(ExportModelAdminMixin, SnippetViewSet):
    raw_id_fields = ("analysis",)  # boost loading speed
    # index_template_name = "FishData/export_csv.html"
    model = FishwayUtility
    menu_label = "魚類使用狀況"
    list_display = (
        "analysis",
        "fish",
        "hour",
        "count",
    )
    list_filter = ("analysis__camera", "analysis__detection_model", "analysis__event_date", "fish", "hour")


class PassCountAdmin(ExportModelAdminMixin, SnippetViewSet):
    raw_id_fields = ("analysis",)  # boost loading speed
    # index_template_name = "FishData/export_csv.html"
    model = PassCount
    menu_label = "魚道通過數"
    list_display = ("analysis", "fish", "count")
    list_filter = ("analysis__camera", "analysis__detection_model", "analysis__event_date", "fish")


class DataGroup(SnippetViewSetGroup):
    menu_label = "魚道監測資料"
    menu_icon = "warning"
    items = (
        TargetFishSpeciesAdmin,
        CameraInfoAdmin,
        DetectionModelInfoAdmin,
        FishwayUtilityAnalysisAdmin,
        FishwayPassAnalysisAdmin,
        FishwayUtilityAdmin,
        PassCountAdmin,
    )


register_snippet(DataGroup)


# register to django admin instead of wagtail admin


class TargetFishSpeciesDjangoAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(TargetFishSpecies, TargetFishSpeciesDjangoAdmin)


class CameraInfoDjangoAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(CameraInfo, CameraInfoDjangoAdmin)


class DetectionModelInfoDjangoAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(DetectionModelInfo, DetectionModelInfoDjangoAdmin)


class FishwayUtilityAnalysisDjangoAdmin(admin.ModelAdmin):
    list_display = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "detection_frequency",
    )
    list_filter = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "detection_frequency",
    )


admin.site.register(FishwayUtilityAnalysis, FishwayUtilityAnalysisDjangoAdmin)


class FishwayPassAnalysisDjangoAdmin(admin.ModelAdmin):
    list_display = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "sample_length",
    )
    list_filter = (
        "camera",
        "detection_model",
        "event_date",
        "analysis_time",
        "sample_length",
    )


admin.site.register(FishwayPassAnalysis, FishwayPassAnalysisDjangoAdmin)


class PassCountDjangoAdmin(admin.ModelAdmin):
    list_display = ("analysis", "fish", "count")
    list_filter = ("analysis__camera", "analysis__detection_model", "analysis__event_date", "fish")


admin.site.register(PassCount, PassCountDjangoAdmin)


class FishwayUtilityDjangoAdmin(admin.ModelAdmin):
    list_display = (
        "analysis",
        "hour",
        "fish",
        "count",
    )
    list_filter = (
        "analysis__camera",
        "analysis__detection_model",
        "analysis__event_date",
        "hour",
        "fish",
    )


admin.site.register(FishwayUtility, FishwayUtilityDjangoAdmin)
