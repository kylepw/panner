from django.http import HttpResponse


def content_view(request, pk):
    return HttpResponse('Line feed for user %s' % str(pk))