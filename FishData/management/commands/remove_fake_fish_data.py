from django.core.management.base import BaseCommand
from FishData.models import *
from django.db import connection

class Command(BaseCommand):
    help = 'remove all fake fish data'
    
    def handle(self, *args, **options):
        TargetFishSpecies.objects.filter(name__startswith="fake_fish_").delete()
        DetectionModelInfo.objects.filter(name="fake_model").delete()
        CameraInfo.objects.filter(name__startswith="fake_camera_").delete()
        # need to vaccum
        cursor = connection.cursor()
        cursor.execute("vacuum;")    
        
        
        