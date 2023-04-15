from django.db import models
from datetime import timedelta

# Create your models here.

class TargetFishSpecies(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='魚種名稱', primary_key=True)
    description = models.TextField(blank=True, verbose_name='描述')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '目標魚種'
        verbose_name_plural = '目標魚種'

class CameraInfo(models.Model):
    class ResolutionChoices(models.TextChoices):
        HD = "HD", ("1280 x 720")
        FHD = "FHD", ("1920 x 1080")
        QHD = "QHD", ("2560 x 1440")
        UHD = "UHD", ("3840 x 2160")
    name = models.CharField(max_length=100, unique=True, verbose_name='監視器名稱', primary_key=True)
    description = models.TextField(blank=True, verbose_name='描述')
    frame_rate = models.FloatField(default=30, verbose_name='影像幀率', help_text='單位為fps')        
    resolution = models.CharField(max_length=100, default=ResolutionChoices.FHD, choices=ResolutionChoices.choices, verbose_name='影像解析度')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '監視器資訊'
        verbose_name_plural = '監視器資訊'

class DetectionModelInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='模型名稱', primary_key=True)
    description = models.TextField(blank=True, verbose_name='描述')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '模型資訊'
        verbose_name_plural = '模型資訊'
    
class FishAnalysis(models.Model):
    class AnyalysisTypes(models.TextChoices):
        DETECTION = "DE", ("偵測")
        COUNT = "CO", ("計數")
    
    camera = models.ForeignKey(CameraInfo, on_delete=models.CASCADE, verbose_name='監視器')
    detection_model = models.ForeignKey(DetectionModelInfo, on_delete=models.CASCADE, verbose_name='模型')
    event_time = models.DateTimeField(verbose_name='事件開始時間')
    event_period = models.DurationField(verbose_name='事件時段', default=timedelta(minutes=5))
    analysis_type = models.CharField(choices=AnyalysisTypes.choices, default=AnyalysisTypes.DETECTION, max_length=2, verbose_name='分析類型')
    analysis_time = models.DateTimeField(verbose_name='分析時間')
    can_anaylze = models.BooleanField(default=True, verbose_name="是否可分析", help_text="如果水體狀況不佳，則不可分析")
    analysis_log = models.TextField(blank=True, verbose_name="分析紀錄", help_text="紀錄分析過程中的特殊狀況")
        
    def __str__(self):
        if self.analysis_type == "DE":
            type_txt = "偵測分析"
        else:
            type_txt = "計數分析"
        if self.can_anaylze:
            can_anaylze_simbol = "O"
        else:
            can_anaylze_simbol = "X"
        return f"{type_txt} ({self.event_time} - {self.camera} - {self.detection_model}) - {can_anaylze_simbol}"
    
    class Meta:
        verbose_name = '魚類分析'
        verbose_name_plural = '魚類分析'

class FishCount(models.Model):
    analysis = models.ForeignKey(FishAnalysis, on_delete=models.CASCADE, verbose_name='分析', related_name='fish_count')
    fish = models.ForeignKey(TargetFishSpecies, on_delete=models.CASCADE, verbose_name='魚種')
    count = models.PositiveIntegerField(default=0, verbose_name='通過數')
    
    def __str__(self):
        return str(self.fish) + " " + str(self.count) 
    class Meta:
        verbose_name = '魚類通過數'
        verbose_name_plural = '魚類通過數'

class FishCountDetail(models.Model):
    analysis = models.ForeignKey(FishAnalysis, on_delete=models.CASCADE, verbose_name='分析', related_name='fish_count_detail')
    fish = models.ForeignKey(TargetFishSpecies, on_delete=models.CASCADE, verbose_name='魚種')
    approximate_speed = models.FloatField(default=0, verbose_name='預估魚類速度', help_text='單位為pixel^2/秒')
    approximate_body_length = models.FloatField(default=0, verbose_name='預估魚體長度', help_text='單位為pixel')
    approximate_body_height = models.FloatField(default=0, verbose_name='預估魚體高度', help_text='單位為pixel')
    enter_frame = models.PositiveIntegerField(default=0, verbose_name='進入時幀數')
    leave_frame = models.PositiveIntegerField(default=0, verbose_name='離開時幀數')
    
    def __str__(self):
        return str(self.fish) + " (" + str(self.enter_frame) + ", " + str(self.leave_frame)+ ")"
    class Meta:
        verbose_name = '魚類通過數細節'
        verbose_name_plural = '魚類通過數細節'
            
    
class FishDetection(models.Model):
    analysis = models.ForeignKey(FishAnalysis, on_delete=models.CASCADE, verbose_name='分析', related_name='fish_detection')
    fish = models.ForeignKey(TargetFishSpecies, on_delete=models.CASCADE, verbose_name='魚種')
    count = models.IntegerField(default=0, verbose_name='數量')
    frame = models.PositiveIntegerField(default=0, verbose_name='幀數')
    can_detect = models.BooleanField(default=True, verbose_name="是否可偵測", help_text="如果水體狀況不佳，則不可偵測")
    
    def __str__(self):
        return str(self.fish) + " " + str(self.count) + " (" + str(self.frame) + ")"
    class Meta:
        verbose_name = '魚類偵測'
        verbose_name_plural = '魚類偵測'
    
        