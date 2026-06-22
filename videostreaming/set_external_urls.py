import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','videostreaming.settings')
import django
django.setup()
from video_streaming.models import Video

mapping = {
    # removed sample-videos big_buck_bunny references
}

for title, url in mapping.items():
    try:
        v = Video.objects.get(title__icontains=title)
        v.external_url = url
        v.save()
        print('Set', v.title, '->', url)
    except Video.DoesNotExist:
        print('No video with title containing', title)
