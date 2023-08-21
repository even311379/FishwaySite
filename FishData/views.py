from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import permissions
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.conf import settings


class TargetFishSpeciesApiView(ModelViewSet):
    queryset = TargetFishSpecies.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TargetFishSpeciesSerializer


class CameraInfoApiView(ModelViewSet):
    queryset = CameraInfo.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CameraInfoSerializer


class DetectionModelInfoApiView(ModelViewSet):
    queryset = DetectionModelInfo.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = DetectionModelInfoSerializer


class FishwayUtilityAnalysisApiView(ModelViewSet):
    queryset = FishwayUtilityAnalysis.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishwayUtilityAnalysisSerializer

    def create(self, request, *args, **kwargs):
        d = request.data
        q = self.queryset.filter(
            event_date=d.get("event_date"), camera=d.get("camera"), detection_model=d.get("detection_model")
        )
        if q:
            serializer = FishwayUtilityAnalysisSerializer(q[0], data=d)
        else:
            serializer = FishwayUtilityAnalysisSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FishwayPassAnalysisApiView(ModelViewSet):
    queryset = FishwayPassAnalysis.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishwayPassAnalysisSerializer

    def create(self, request, *args, **kwargs):
        d = request.data
        q = self.queryset.filter(
            event_date=d.get("event_date"), camera=d.get("camera"), detection_model=d.get("detection_model")
        )
        if q:
            serializer = FishwayPassAnalysisSerializer(q[0], data=d)
        else:
            serializer = FishwayPassAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FishwayUtilityApiView(ModelViewSet):
    queryset = FishwayUtility.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishwayUtilitySerializer

    def get_analysis_id(self, camera_name, target_date):
        analysis = FishwayUtilityAnalysis.objects.filter(camera=camera_name, event_date=target_date)
        return analysis[0].pk

    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return super().create(request, *args, **kwargs)
        all_data = []
        for d in request.data:
            data = {
                "analysis": self.get_analysis_id(d.get("camera"), d.get("event_date")),
                "fish": d.get("fish"),
                "hour": d.get("hour"),
                "count": d.get("count"),
            }
            all_data.append(data)

        serializer = FishwayUtilitySerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassCountApiView(ModelViewSet):
    queryset = PassCount.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PassCountSerializer

    def get_analysis_id(self, camera_name, target_date):
        analysis = FishwayPassAnalysis.objects.filter(camera=camera_name, event_date=target_date)
        return analysis[0].pk

    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return super().create(request, *args, **kwargs)

        all_data = []
        for d in request.data:
            data = {
                "analysis": self.get_analysis_id(d.get("camera"), d.get("event_date")),
                "fish": d.get("fish"),
                "count": d.get("count"),
            }
            all_data.append(data)

        serializer = PassCountSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FishCountDetailApiView(ModelViewSet):
#     queryset = FishCountDetail.objects.all()
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     serializer_class = FishCountDetailSerializer
#
#     def create(self, request, *args, **kwargs):
#         if type(request.data) != list:
#             return super().create(self, request, *args, **kwargs)
#         all_data = []
#         for d in request.data:
#             data = {
#                 "analysis": get_analysis_id(d.get("analysis"), "CO"),
#                 "fish": d.get("fish"),
#                 "approximate_speed": d.get("approximate_speed"),
#                 "approximate_body_length": d.get("approximate_body_length"),
#                 "approximate_body_height": d.get("approximate_body_height"),
#                 "enter_frame": d.get("enter_frame"),
#                 "leave_frame": d.get("leave_frame"),
#             }
#             all_data.append(data)
#
#         serializer = FishCountDetailSerializer(data=all_data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
