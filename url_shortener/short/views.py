from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .models import ShortURL


def home(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url', '').strip()
        if not original_url:
            return render(request, 'short/home.html', {'error': 'Please enter a valid URL.'})

        short_url_obj, _ = ShortURL.objects.get_or_create(original_url=original_url)
        short_url = request.build_absolute_uri(f'/{short_url_obj.short_code}/')
        return render(request, 'short/home.html', {'short_url': short_url})

    return render(request, 'short/home.html')


def redirect_to_url(request, short_code):
    short_url_obj = get_object_or_404(ShortURL, short_code=short_code)
    return HttpResponseRedirect(short_url_obj.original_url)
