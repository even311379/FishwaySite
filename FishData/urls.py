from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    # this is how to retrive data from url.. not necessary for now
    # re_path(r'target_fish_species/?page=(?P<page>\d+)', TargetFishSpeciesApiView.as_view()),
    
    # so weird name conflict with wagtail Can not use 'target_fish_species'
    path("target_fish_species", TargetFishSpeciesApiView.as_view()), 
    path('camera_info', CameraInfoApiView.as_view()),
    path('detection_model_info', DetectionModelInfoApiView.as_view()),
    path('fish_analysis', FishAnalysisApiView.as_view()),
    path('fish_count', FishCountApiView.as_view()),
    path('fish_count_detail', FishCountDetailApiView.as_view()),
    path('fish_detection', FishDetectionApiView.as_view()),
]