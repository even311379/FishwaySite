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


class FishwayUtilityAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishwayUtilityAnalysis
        fields = "__all__"


class FishwayPassAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishwayPassAnalysis
        fields = "__all__"


class PassCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassCount
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["analysis"] = str(instance.analysis)  # use str to replace FK id
        return data


class FishwayUtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FishwayUtility
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["analysis"] = str(instance.analysis)  # use str to replace FK id
        return data
