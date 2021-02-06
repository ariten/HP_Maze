import json
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    """The page the user sees when they load the site."""
    return render(request, "maze/index.html")


def register_team(request):
    """Takes the user's input of team name and stores it in the session as the user's unique ID."""
    if request.is_ajax() and request.method == 'POST':
        team_name = request.POST.get("userInput", "")
        print("User registered team %s" % team_name)
        request.session["userID"] = team_name
        return JsonResponse({"success": True, "teamName": request.session["userID"]})
    return JsonResponse({"success": False})


def test_json_call(request):
    """Used to test a vertical slice of the stack."""
    print(request)
    if request.is_ajax() and request.method == 'POST':
        print(request.body)
        data = request.POST.get("userInput", "")
        userID = request.session["userID"]
        print("User from %s submitted %s" % (userID, data))
    return JsonResponse({"direction": "North", "distance": 10})
