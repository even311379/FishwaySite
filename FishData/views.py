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

class FishAnalysisApiView(ModelViewSet):
    queryset = FishAnalysis.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    serializer_class = FishAnalysisSerializer
    
    def create(self, request, *args, **kwargs):
        if type(request.data) == list:
            return super().create(request, *args, **kwargs)
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

# TODO: need test
def get_analysis_id(analysis_string, analysis_type="DE"):
    camera, detection_model, event_time_string = analysis_string.split(',')
    print(event_time_string)
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

class FishCountApiView(ModelViewSet):
    queryset = FishCount.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishCountSerializer
    
    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return super().create(request, *args, **kwargs)
            
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

class FishCountDetailApiView(ModelViewSet):
    queryset = FishCountDetail.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishCountDetailSerializer
    
    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return super().create(self, request, *args, **kwargs)
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

class FishDetectionApiView(ModelViewSet):
    queryset = FishDetection.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FishDetectionSerializer

    # TODO: leave filter function in the future or never?
    # def get_queryset(self):
    #     return FishDetection.objects.all()

    def create(self, request, *args, **kwargs):
        if type(request.data) != list:
            return super().create(request, *args, **kwargs)
        all_data = []
        for d in request.data:
            data = {
                'analysis': get_analysis_id(d.get('analysis'), "DE"),
                'fish': d.get('fish'),
                'count': d.get('count'),
                'detect_time': d.get('detect_time'),
                'can_detect': d.get('can_detect'),
            }
            all_data.append(data)

        serializer = FishDetectionSerializer(data=all_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
