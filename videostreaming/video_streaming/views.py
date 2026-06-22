from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse, Http404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

# Prefer `requests` if installed, but fall back to stdlib `urllib` when missing.
try:
	import requests as _requests
except Exception:
	_requests = None
import urllib.request
import urllib.error
import os
from django.conf import settings
from django import forms
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Video, Audio, Playlist


class HomeView(TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['latest_videos'] = Video.objects.order_by('-created_at')[:4]
		ctx['popular_videos'] = Video.objects.order_by('-views_count')[:3]
		ctx['playlists'] = Playlist.objects.all()[:6]
		return ctx


class VideoListView(ListView):
	model = Video
	template_name = 'video_list.html'
	context_object_name = 'videos'


class VideoPlayerView(DetailView):
	model = Video
	template_name = 'video_player.html'

	def get(self, request, *args, **kwargs):
		try:
			return super().get(request, *args, **kwargs)
		except Http404:
			# If the video doesn't exist, redirect to the video list instead of showing DEBUG 404
			return redirect('video_streaming:video_list')

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		v = self.object
		# Determine player src: prefer uploaded file, otherwise proxy to external_url
		file_url = v.file.url if v.file else ''
		external = v.external_url or ''
		autoplay = self.request.GET.get('autoplay') == '1'
		now = int(__import__('time').time())
		# Prefer external URL (proxied) when provided so user-supplied URL plays immediately
		if external:
			src = reverse('video_streaming:video_proxy', kwargs={'pk': v.pk})
		elif file_url:
			src = file_url
		else:
			src = ''

		# Append cache-busting timestamp when autoplay requested so browser refetches
		if src and autoplay:
			sep = '&' if '?' in src else '?'
			src = f"{src}{sep}_cb={now}"
		print(f"[player_context] video={v.pk} src={src} autoplay={autoplay}")

		# Build a list of available media files for this video (uploaded file + any matching files in media/videos)
		media_files = []
		if v.file:
			media_files.append({'url': v.file.url, 'name': os.path.basename(v.file.name)})
		# scan MEDIA_ROOT/videos for files whose name contains any title word or the video pk
		title = (v.title or '').lower()
		title_words = [w for w in ''.join((ch if ch.isalnum() else ' ') for ch in title).split() if w]
		video_pk_str = str(v.pk)
		videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
		try:
			for fname in os.listdir(videos_dir):
				if not fname:
					continue
				# skip file already listed
				if v.file and fname == os.path.basename(v.file.name):
					continue
				fn_lower = fname.lower()
				# match if any title word appears in filename, or pk appears in filename
				if (any(w in fn_lower for w in title_words) or video_pk_str in fn_lower):
					media_files.append({'url': settings.MEDIA_URL.rstrip('/') + '/videos/' + fname, 'name': fname})
		except Exception:
			# ignore if MEDIA_ROOT not available or directory missing
			pass

		ctx['media_files'] = media_files
		ctx['player_src'] = src
		ctx['player_autoplay'] = autoplay
		ctx['player_now'] = now
		return ctx


# Use a ModelForm so we can add widget attributes (placeholder for external_url)
class VideoForm(forms.ModelForm):
	class Meta:
		model = Video
		fields = ['title', 'description', 'file', 'external_url']
		widgets = {
			'external_url': forms.URLInput(attrs={'placeholder': 'https://cdn.example.com/video.mp4'})
		}


class VideoCreateView(CreateView):
	model = Video
	form_class = VideoForm
	template_name = 'video_form.html'

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.uploaded_by = self.request.user
		response = super().form_valid(form)
		file_url = form.instance.file.url if form.instance.file else ''
		ext = form.instance.external_url or ''
		print(f"[video_create] saved id={form.instance.pk} external_url={ext} file={file_url}")
		messages.success(self.request, 'Video created.')

		# Render the player page immediately with autoplay (avoid redirect)
		v = form.instance
		# Prefer external_url over uploaded file when immediately rendering player
		src = (reverse('video_streaming:video_proxy', kwargs={'pk': v.pk}) if v.external_url else (v.file.url if v.file else ''))
		now = int(__import__('time').time())
		if src:
			sep = '&' if '?' in src else '?'
			src = f"{src}{sep}_cb={now}"
		context = {
			'object': v,
			'player_src': src,
			'player_autoplay': True,
			'player_now': now,
		}
		return render(self.request, 'video_player.html', context)

	def get_success_url(self):
		return reverse('video_streaming:video_player', kwargs={'pk': self.object.pk}) + '?autoplay=1'


class VideoUpdateView(UpdateView):
	model = Video
	form_class = VideoForm
	template_name = 'video_form.html'

	def get_success_url(self):
		return reverse('video_streaming:video_player', kwargs={'pk': self.object.pk}) + '?autoplay=1'
	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.uploaded_by = self.request.user
		response = super().form_valid(form)
		# Log and show a success message with current sources
		file_url = form.instance.file.url if form.instance.file else ''
		ext = form.instance.external_url or ''
		print(f"[video_update] saved id={form.instance.pk} external_url={ext} file={file_url}")
		messages.success(self.request, 'Video saved.')

		# Render the player page immediately with autoplay (avoid redirect)
		v = form.instance
		# Prefer external_url over uploaded file when immediately rendering player
		src = (reverse('video_streaming:video_proxy', kwargs={'pk': v.pk}) if v.external_url else (v.file.url if v.file else ''))
		now = int(__import__('time').time())
		if src:
			sep = '&' if '?' in src else '?'
			src = f"{src}{sep}_cb={now}"
		context = {
			'object': v,
			'player_src': src,
			'player_autoplay': True,
			'player_now': now,
		}
		return render(self.request, 'video_player.html', context)


class VideoDeleteView(DeleteView):
	model = Video
	template_name = 'video_confirm_delete.html'
	success_url = reverse_lazy('video_streaming:video_list')


class AudioPlayerView(DetailView):
	model = Audio
	template_name = 'audio_player.html'


class PlaylistView(ListView):
	model = Playlist
	template_name = 'playlist.html'
	context_object_name = 'playlists'


class PlaylistCreateView(CreateView):
	model = Playlist
	fields = ['name', 'videos']
	template_name = 'playlist_form.html'
	success_url = reverse_lazy('video_streaming:playlist_list')

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.owner = self.request.user
		else:
			# fallback to first user if anonymous
			from django.contrib.auth import get_user_model
			User = get_user_model()
			form.instance.owner = User.objects.first()
		return super().form_valid(form)


class PlaylistUpdateView(UpdateView):
	model = Playlist
	fields = ['name', 'videos']
	template_name = 'playlist_form.html'
	success_url = reverse_lazy('video_streaming:playlist_list')


class PlaylistDeleteView(DeleteView):
	model = Playlist
	template_name = 'playlist_confirm_delete.html'
	success_url = reverse_lazy('video_streaming:playlist_list')


class PlaylistDetailView(DetailView):
	model = Playlist
	template_name = 'playlist_detail.html'


def SearchView(request):
	q = request.GET.get('q', '')
	videos = Video.objects.filter(title__icontains=q) if q else Video.objects.none()
	audios = Audio.objects.filter(title__icontains=q) if q else Audio.objects.none()
	return render(request, 'search_results.html', {
		'query': q,
		'videos': videos,
		'audios': audios
	})

def file_list(request):
	files = Video.objects.all()
	return render(request, 'file_list.html', {'files': files})


def video_meta(request, pk):
	"""Return current media URLs for a video as JSON."""
	v = get_object_or_404(Video, pk=pk)
	file_url = v.file.url if v.file else ''
	external = v.external_url or ''
	return JsonResponse({'file_url': file_url, 'external_url': external, 'now': int(__import__('time').time())})


@require_GET
def proxy_stream(request, pk):
	"""Proxy an external video URL through the Django app so playback always fetches fresh content.

	This forwards Range requests when present to allow seeking.
	"""
	v = get_object_or_404(Video, pk=pk)
	url = v.external_url
	if not url:
		return HttpResponse('No external URL configured for this video', status=404)

	# Forward Range header if client provided one (for seeking)
	headers = {}
	range_header = request.headers.get('Range') or request.META.get('HTTP_RANGE')
	if range_header:
		headers['Range'] = range_header

	if _requests:
		try:
			print(f"[video_proxy] proxying id={pk} -> {url} headers={headers}")
			upstream = _requests.get(url, stream=True, headers=headers, timeout=15)
		except _requests.RequestException as exc:
			print(f"[video_proxy] upstream request failed for id={pk} url={url} error={exc}")
			return HttpResponse('Upstream fetch failed', status=502)

		iterator = upstream.iter_content(chunk_size=8192)
		status = upstream.status_code
		upstream_headers = upstream.headers
	else:
		# Fallback to urllib
		try:
			print(f"[video_proxy] proxying id={pk} -> {url} headers={headers}")
			req = urllib.request.Request(url, headers=headers)
			uresp = urllib.request.urlopen(req, timeout=15)
		except Exception as exc:
			print(f"[video_proxy] upstream request failed for id={pk} url={url} error={exc}")
			return HttpResponse('Upstream fetch failed', status=502)

		def iterator():
			try:
				while True:
					chunk = uresp.read(8192)
					if not chunk:
						break
					yield chunk
			finally:
				try:
					uresp.close()
				except Exception:
					pass

		status = uresp.getcode()
		# urllib response headers: getheaders() -> list of tuples
		upstream_headers = {k: v for k, v in uresp.getheaders()}

	# Stream upstream response back to client
	resp = StreamingHttpResponse(iterator(), status=status)
	# Copy some useful headers
	content_type = upstream_headers.get('Content-Type')
	if content_type:
		resp['Content-Type'] = content_type
	# Range/Content-Range / Accept-Ranges
	if 'Content-Range' in upstream_headers:
		resp['Content-Range'] = upstream_headers['Content-Range']
	if 'Accept-Ranges' in upstream_headers:
		resp['Accept-Ranges'] = upstream_headers['Accept-Ranges']

	# Prevent caching at the browser so we always fetch fresh data when requested
	resp['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	resp['Pragma'] = 'no-cache'
	resp['Expires'] = '0'

	return resp


@require_POST
def remove_video(request, pk):
	"""Permanently delete a Video and its uploaded file.

	Only the uploader or staff may delete.
	"""
	v = get_object_or_404(Video, pk=pk)
	user = request.user
	# Permission: uploader or staff
	if not user.is_authenticated or not (user.is_staff or (v.uploaded_by and v.uploaded_by == user)):
		return HttpResponseForbidden('Permission denied')

	# Delete uploaded file from storage if present
	try:
		if v.file:
			v.file.delete(save=False)
	except Exception as exc:
		print(f"[remove_video] error deleting file for id={pk}: {exc}")

	v.delete()
	return JsonResponse({'deleted': True})
