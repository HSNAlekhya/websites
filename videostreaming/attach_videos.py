import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','videostreaming.settings')
import django
django.setup()
from django.core.files import File
from video_streaming.models import Video

base = os.path.dirname(os.path.abspath(__file__))
maplist = [
    ('Introduction to Django', os.path.join(base,'media','videos','introduction_to_django.mp4')),
    ('Building a Video Player', os.path.join(base,'media','videos','building_a_video_player.mp4')),
    ('Streaming Basics', os.path.join(base,'media','videos','streaming_basics.mp4')),
    ('Responsive Video Layouts', os.path.join(base,'media','videos','responsive_video_layouts.mp4')),
    ('Optimizing Media', os.path.join(base,'media','videos','optimizing_media.mp4')),
]

for title, path in maplist:
    try:
        v = Video.objects.get(title=title)
        if os.path.exists(path):
            with open(path,'rb') as f:
                django_file = File(f)
                v.file.save(os.path.basename(path), django_file, save=True)
            print(f"Attached {path} to '{title}'")
        else:
            print(f"File not found: {path}")
    except Video.DoesNotExist:
        print(f"Video record not found for title: {title}")
