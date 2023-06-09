from rest_framework import serializers

from .models import *

class TargetFishSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetFishSpecies
        fields = "__all__"

class CameraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraInfo
        fields = "__all__"
        
class DetectionModelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionModelInfo
        fields = "__all__"        
        
        
class FishAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishAnalysis
        fields = "__all__"

class FishCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishCount
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['analysis'] = str(instance.analysis) # use str to replace FK id
        return data
        
class FishCountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishCountDetail
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['analysis'] = str(instance.analysis) # use str to replace FK id
        return data
        
class FishDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishDetection
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['analysis'] = str(instance.analysis) # use str to replace FK id
        return data