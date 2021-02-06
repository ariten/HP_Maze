from django.shortcuts import render

def index(request):
    """The page the user sees when they load the site."""
    return render(request, "maze/index.html")
