from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from video_streaming.models import Video, Playlist
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Create sample user, videos and playlists'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='sampleuser')
        if created:
            user.set_password('password')
            user.save()

        # create sample videos
        vids = []
        sample_data = [
            ('Introduction to Django', 'A short intro.'),
            ('Building a Video Player', 'How to build a player.'),
            ('Streaming Basics', 'Concepts and patterns.'),
            ('Responsive Video Layouts', 'Layouts for all devices.'),
            ('Optimizing Media', 'Optimization tips.'),
        ]
        for i, (title, desc) in enumerate(sample_data, start=1):
            v, _ = Video.objects.get_or_create(title=title, defaults={'description': desc, 'uploaded_by': user})
            v.views_count = (6 - i) * 10  # some view counts
            v.save()
            vids.append(v)

        # create playlists
        p1, _ = Playlist.objects.get_or_create(name='Beginner Tutorials', owner=user)
        p1.videos.set(vids[:3])
        p1.save()

        p2, _ = Playlist.objects.get_or_create(name='Media Tools', owner=user)
        p2.videos.set(vids[2:5])
        p2.save()

        self.stdout.write(self.style.SUCCESS('Sample data created (user: sampleuser, password: password)'))
