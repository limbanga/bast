from django.shortcuts import render
from django.template import RequestContext

PREFIX = "errors/"


# TODO: Define handler404 and handler500 views
def handler500(request, *args, **argv):
    response = render(
        request,
        f"{PREFIX}500.html",
        {},
    )
    response.status_code = 500
    return response


def handler404(request, exception):
    response = render(request, f"{PREFIX}404.html", {})
    response.status_code = 404
    return response
