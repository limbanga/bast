from django.shortcuts import render

def error_404_view(request, exception):
    return render(request, 'error/404.html', status=404)