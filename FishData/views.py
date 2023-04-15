from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import permissions
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from django.conf import settings


class TargetFishSpeciesApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        # print(self.kwargs)
        items = TargetFishSpecies.objects.all()
        serializer = TargetFishSpeciesSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CameraInfoApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        camera_info = CameraInfo.objects.all()
        serializer = CameraInfoSerializer(camera_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DetectionModelInfoApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        detection_model_info = DetectionModelInfo.objects.all()
        serializer = DetectionModelInfoSerializer(detection_model_info, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FishAnalysisApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        fish_analysis = FishAnalysis.objects.all()
        serializer = FishAnalysisSerializer(fish_analysis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        all_data = []
        for d in request.data:
            data = {
                'camera': d.get('camera'),
                'detection_model': d.get('detection_model'),
                'event_time': d.get('event_time'),
                'event_period': d.get('event_period'),
                'analysis_type': d.get('analysis_type'),
                'analysis_time': d.get('analysis_time'),
                'can_analysis': d.get('can_analysis'),
                'analysis_log': d.get('analysis_log'),
            }
            all_data.append(data)

        serializer = FishAnalysisSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# todo: need test
def get_analysis_id(analysis_string, analysis_type="DE"):
    camera, detection_model, event_time_string = analysis_string.split(',')
    event_time = datetime.strptime(event_time_string, '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo(settings.TIME_ZONE))
    
    analysis = FishAnalysis.objects.filter(
        camera=camera,
        detection_model=detection_model,
        event_time=event_time,
        analysis_type=analysis_type,
    )
    if analysis.exists():
        print(analysis[0].pk)
        return analysis[0].pk
    else:
        print('analysis not found')
        return None

class FishCountApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        fish_count = FishCount.objects.all()
        serializer = FishCountSerializer(fish_count, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        all_data = []
        for d in request.data:
            data = {
                'analysis': get_analysis_id(d.get('analysis'), "CO"),
                'fish': d.get('fish'),
                'count': d.get('count'),
            }
            all_data.append(data)

        serializer = FishCountSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FishCountDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        fish_count_detail = FishCountDetail.objects.all()
        serializer = FishCountDetailSerializer(fish_count_detail, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        all_data = []
        for d in request.data:
            data = {
                'analysis': get_analysis_id(d.get('analysis'), "CO"),
                'fish': d.get('fish'),
                'approximate_speed': d.get('approximate_speed'),
                'approximate_body_length': d.get('approximate_body_length'),
                'approximate_body_height': d.get('approximate_body_height'),
                'enter_frame': d.get('enter_frame'),
                'leave_frame': d.get('leave_frame'),
            }
            all_data.append(data)

        serializer = FishCountDetailSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FishDetectionApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request):
        fish_detection = FishDetection.objects.all()
        serializer = FishCountSerializer(fish_detection, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        all_data = []
        for d in request.data:
            data = {
                'analysis': get_analysis_id(d.get('analysis'), "DE"),
                'fish': d.get('fish'),
                'count': d.get('count'),
                'frame': d.get('frame'),
                'can_detect': d.get('can_detect'),
            }
            all_data.append(data)

        serializer = FishDetectionSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
