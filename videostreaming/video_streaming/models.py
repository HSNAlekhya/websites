from django.db import models
from django.conf import settings


class Video(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	file = models.FileField(upload_to="videos/")
	views_count = models.PositiveIntegerField(default=50)
	external_url = models.URLField(blank=True, null=True)
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Audio(models.Model):
	title = models.CharField(max_length=255)
	file = models.FileField(upload_to="audios/")
	uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Playlist(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	videos = models.ManyToManyField(Video, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class WatchHistory(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	video = models.ForeignKey(Video, on_delete=models.CASCADE)
	watched_at = models.DateTimeField(auto_now_add=True)
	progress = models.FloatField(default=0.0)

	class Meta:
		verbose_name = "Watch History"
		verbose_name_plural = "Watch Histories"

	def __str__(self):
		return f"{self.user} - {self.video} @ {self.progress}"
