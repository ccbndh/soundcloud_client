from django.http import JsonResponse
from spiders.soundcloud import SoundCloudCL


def search(request):
    return JsonResponse(SoundCloudCL.search(request.GET.get('q')))


def top(request):
    return JsonResponse(SoundCloudCL.top_50())


def song(request):
    return JsonResponse(SoundCloudCL.song(request.GET.get('url')))
