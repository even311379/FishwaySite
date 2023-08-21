from django.db import models
from datetime import timedelta
from django.conf import settings
from zoneinfo import ZoneInfo

from wagtail.contrib.settings.models import BaseGenericSetting, register_setting

# Create your models here.


# TODO: is task runing notify...
@register_setting(icon="placeholder")
class TaskNotification(BaseGenericSetting):
    is_scheduled_task_running = models.BooleanField(default=False)

    class Meta:
        verbose_name = "自動化是否啟動？"


class TargetFishSpecies(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="魚種名稱", primary_key=True)
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "目標魚種"
        verbose_name_plural = "目標魚種"


class CameraInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="監視器名稱", primary_key=True)
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "監視器資訊"
        verbose_name_plural = "監視器資訊"


class DetectionModelInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="模型名稱", primary_key=True)
    description = models.TextField(blank=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "模型資訊"
        verbose_name_plural = "模型資訊"


class FishAnalysis(models.Model):
    camera = models.ForeignKey(CameraInfo, on_delete=models.CASCADE, verbose_name="監視器")
    detection_model = models.ForeignKey(DetectionModelInfo, on_delete=models.CASCADE, verbose_name="模型")
    event_date = models.DateField(verbose_name="事件開始時間")
    analysis_time = models.DateTimeField(verbose_name="分析時間")
    analysis_log = models.TextField(blank=True, verbose_name="分析紀錄", help_text="紀錄分析過程中的特殊狀況")

    class Meta:
        abstract = True


class FishwayUtilityAnalysis(FishAnalysis):
    detection_frequency = models.PositiveIntegerField(default=1, verbose_name="偵測頻度(幾秒一次)")

    def __str__(self):
        return f"Utility analysis - {self.camera} - {self.event_date.strftime('%Y%m%d')}"

    class Meta:
        ordering = ["-event_date"]
        verbose_name = "魚道使用分析"
        verbose_name_plural = "魚道使用分析"


class FishwayPassAnalysis(FishAnalysis):
    sample_length = models.PositiveIntegerField(default=10, verbose_name="取樣長度（每小時幾分鐘）")

    def __str__(self):
        return f"Pass analysis - {self.camera} - {self.event_date.strftime('%Y%m%d')}"

    class Meta:
        ordering = ["-event_date"]
        verbose_name = "魚道通過分析"
        verbose_name_plural = "魚道通過分析"


class FishwayUtility(models.Model):
    analysis = models.ForeignKey(
        FishwayUtilityAnalysis, on_delete=models.CASCADE, verbose_name="分析", related_name="fishway_utility"
    )
    fish = models.ForeignKey(TargetFishSpecies, on_delete=models.CASCADE, verbose_name="魚種")
    hour = models.PositiveIntegerField(verbose_name="偵測時間", default=0, help_text="當天哪個小時的平均？")
    count = models.FloatField(default=0, verbose_name="平均數量")

    def __str__(self):
        return str(self.fish) + " " + str(self.count) + " (" + str(self.hour) + ")"

    class Meta:
        ordering = ["-analysis"]
        verbose_name = "魚類使用狀況"
        verbose_name_plural = "魚類使用狀況"


class PassCount(models.Model):
    analysis = models.ForeignKey(
        FishwayPassAnalysis, on_delete=models.CASCADE, verbose_name="分析", related_name="pass_count"
    )
    fish = models.ForeignKey(TargetFishSpecies, on_delete=models.CASCADE, verbose_name="魚種")
    count = models.PositiveIntegerField(default=0, verbose_name="隻數")

    def __str__(self):
        return str(self.fish) + " " + str(self.count)

    class Meta:
        ordering = ["-analysis"]
        verbose_name = "魚類通過數"
        verbose_name_plural = "魚類通過數"
