from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('target_fish_species', TargetFishSpeciesApiView)
router.register('camera_info', CameraInfoApiView)
router.register('detection_model_info', DetectionModelInfoApiView)
router.register('fish_analysis', FishAnalysisApiView)
router.register('fish_count', FishCountApiView)
router.register('fish_count_detail', FishCountDetailApiView)
router.register('fish_detection', FishDetectionApiView)

urlpatterns = [
    path('', include(router.urls)),
]