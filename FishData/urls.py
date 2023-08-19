from django.urls import path, include, re_path
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register("target_fish_species", TargetFishSpeciesApiView)
router.register("camera_info", CameraInfoApiView)
router.register("detection_model_info", DetectionModelInfoApiView)
router.register("fishway_utility_analysis", FishwayUtilityAnalysisApiView)
router.register("fishway_pass_analysis", FishwayPassAnalysisApiView)
router.register("pass_count", PassCountApiView)
router.register("fishway_utility", FishwayUtilityApiView)

urlpatterns = [
    path("", include(router.urls)),
]
