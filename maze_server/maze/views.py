from django.shortcuts import render

from maze_handler.MazeHandler import MazeHandler


def index(request):
    mh = MazeHandler()

    return render(request, "maze/index.html")
