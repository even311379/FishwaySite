from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from FishData.models import *
import random

class Command(BaseCommand):
    help = 'create fake fish data for testing'

    def add_arguments(self, parser):
        parser.add_argument("--n_species", nargs='?', type=int, help="number of fake species")
        parser.add_argument("--n_camera", nargs='?', type=int, help="number of fake camera")
        parser.add_argument("--start_date", nargs='?', type=str, help="start date of fake data in this format: YYYY-MM-DD")
        parser.add_argument("--end_date", nargs='?', type=str, help="end data of fale data in this format: YYYY-MM-DD")
        parser.add_argument("--detection_gap", nargs='?', default=10, type=int, help="gap between detection in seconds")

    def handle(self, *args, **options):
        n_species = options["n_species"]
        n_camera = options["n_camera"]
        start_date = datetime.strptime(options["start_date"], "%Y-%m-%d").replace(tzinfo=ZoneInfo('Asia/Taipei'))
        end_date = datetime.strptime(options["end_date"], "%Y-%m-%d").replace(tzinfo=ZoneInfo('Asia/Taipei'))
        
        temp = []
        for i in range(n_species):
            temp.append(TargetFishSpecies(
                name=f"fake_fish_{i}",
                description="this is fake species for testing",
                ))
        fake_species = TargetFishSpecies.objects.bulk_create(temp)

        # just decay from climax time per hour
        climax_time_options = [9, 15]
        max_options = [7, 8, 9, 10]
        decay_rate_options = [0.05, 0.06, 0.08, 0.1]
        fake_species_params = {}
        for s in fake_species:
            fake_species_params[s] = dict(
                climax_time=random.choice(climax_time_options),
                max_in_screen=random.choice(max_options),
                decay=random.choice(decay_rate_options),
            )
            
        temp = []
        for i in range(n_camera):
            temp.append(CameraInfo(
                name=f"fake_camera_{i}",
                description="this is fake camera for testing",
                frame_rate=30,
                resolution="FHD",
                ))
        fake_cameras = CameraInfo.objects.bulk_create(temp)
            
        fake_model = DetectionModelInfo(name="fake_model", description="this is fake model for testing")
        fake_model.save()
        
        temp = []
        for d in range((end_date - start_date).days):
            for h in range(6, 19):
                event_time = start_date + timedelta(days=d, hours=h)
                for c in fake_cameras:
                    temp.append(FishAnalysis(
                        camera=c,
                        detection_model=fake_model,
                        event_time=event_time,
                        event_period=timedelta(minutes=10),
                        analysis_type="CO",
                        analysis_time=event_time+timedelta(hours=12),
                        can_analyze=True,
                        analysis_log="this is fake analysis log",
                    ))
            for c in fake_cameras:
                temp.append(FishAnalysis(
                    camera=c,
                    detection_model=fake_model,
                    event_time=start_date + timedelta(days=d, hours=6),
                    event_period=timedelta(hours=12),
                    analysis_type="DE",
                    analysis_time=start_date + timedelta(days=d, hours=18),
                    can_analyze=True,
                    analysis_log="this is fake analysis log",
                ))
        fake_analysis = FishAnalysis.objects.bulk_create(temp)
        for a in fake_analysis:
            a.save()
        
        random_deviate_options = [0.3, 0.5 ,0.7, 0.9]
        random_frames_to_pass_options = [60, 90, 120, 150, 180, 210] # assume the required frames to pass the fishway
        
        count_result = []
        count_details = []
        detection_result = []
        for analysis in fake_analysis:            
            if analysis.analysis_type == "CO":
                # lazy... just let it all be 10
                for species in fake_species:
                    climax_time = fake_species_params[species]['climax_time']
                    decay = fake_species_params[species]['decay']
                    max_in_screen = fake_species_params[species]['max_in_screen']
                    deviate  = random.choice(random_deviate_options)
                    count = max_in_screen * (1 - decay * abs((i/30/60/60) - climax_time)) * 30 * 60 * 10 / random.choice(random_frames_to_pass_options)
                    count = round(random.uniform(count * (1 - deviate), count * (1 + deviate)))
                    count = min(max(0, count), 100)
                    count_result.append(FishCount(
                        analysis=analysis,
                        fish=species,
                        count=count,
                    ))
                    # store every count detail    
                    for i in range(count):
                        enter_frame = random.randint(0, 30*60*10 - 60)
                        count_details.append(FishCountDetail(
                            analysis=analysis,
                            fish = species,
                            approximate_speed = random.uniform(0, 10),
                            approximate_body_length = random.uniform(0, 10),
                            approximate_body_height = random.uniform(0, 10),
                            enter_frame = enter_frame,
                            leave_frame = enter_frame + random.randint(10, 60),
                        ))                                            
            else:
                for species in fake_species:
                    # every 10 senconds (2160 times per day?)??
                    for h in range(6, 19):
                        for m in range(60):
                            for s in range(0, 60, 10):
                                climax_time = fake_species_params[species]['climax_time']
                                decay = fake_species_params[species]['decay']
                                max_in_screen = fake_species_params[species]['max_in_screen']
                                count = max_in_screen * (1 - decay * abs(h - climax_time))
                                deviate  = random.choice(random_deviate_options)
                                count = round(random.uniform(count*(1-deviate), count*(1+deviate)))
                                if count <= 0:
                                    continue
                                detection_result.append(FishDetection(
                                    analysis=analysis,
                                    fish=species,
                                    detect_time=time(h, m, s),
                                    count=count,
                                ))
                        
        FishCount.objects.bulk_create(count_result)
        FishCountDetail.objects.bulk_create(count_details)
        FishDetection.objects.bulk_create(detection_result)