from django.http import HttpResponse


def content_view(request, pk):
    return HttpResponse('Spotify feed for user %s' % str(pk))