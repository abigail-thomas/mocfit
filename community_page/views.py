from django.shortcuts import render


def index(request):
    return render(request, 'community_page/index.html')
