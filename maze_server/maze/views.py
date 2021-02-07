import json
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import GameStart, Team

DEBUG = True

def index(request):
    """The page the user sees when they load the site."""
    # Check to see if the user has selected a team yet, if not redirect to the selection page
    if "user_id" not in request.session:
        return redirect('team_selection')

    user_id = request.session["user_id"]
    return render(request, "maze/index.html", {"user_id": user_id})


def team_selection(request):
    """Provide the user with a dropdown from which they select their team, then redirect them to the main page on success."""
    # Get all of the teams
    all_teams = Team.objects.all()
    print(all_teams)
    context = {"teams": all_teams}
    return render(request, "maze/team_selection.html", context)


def api_register_team(request):
    """Takes the user's input of team name and stores it in the session as the user's unique ID."""
    if request.is_ajax() and request.method == 'POST':
        team_name = request.POST.get("userSelection", "")
        print("User selected team %s" % team_name)
        request.session["user_id"] = team_name
        return JsonResponse({"success": True, "teamName": request.session["user_id"]})
    return JsonResponse({"success": False})


def api_user_input(request):
    """Process a command line command sent by the user."""
    user_id = request.session["user_id"]
    if request.is_ajax() and request.method == 'POST':
        user_input = request.POST.get("userInput", "")
        print("User from %s submitted %s" % (user_id, user_input))

        if not DEBUG:
            game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
            if datetime.now() < game_start_time:
                return JsonResponse({
                    "success": True,
                    "terminalLine": "The game has not started yet.",
                    "lockout": False,
                    "lockoutDuration": 0
            })

            game_end_time = game_start_time + timedelta(minutes=15)
            if datetime.now() > game_end_time:
                return JsonResponse({
                    "success": True,
                    "terminalLine": "You are too late, the game has ended.",
                    "lockout": False,
                    "lockoutDuration": 0
            })

        # Do something with the input and get a response text line
        output = "Example output line, " + user_input

        reply_data = {
            "success": True,
            "terminalLine": output,
            "lockout": True,
            "lockoutDuration": 10
        }

        return JsonResponse(reply_data)

    else:
        return JsonResponse({"success": False})


def api_time_until_start(request):
    """Return the time in seconds until the game starts."""
    if request.is_ajax() and request.method == 'GET':
        game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
        time_remaining = game_start_time - datetime.now()
        delta = int(time_remaining.total_seconds())

        if delta > 0:
            return JsonResponse({"gameStarted": False, "duration": delta})
        else:
            return JsonResponse({"gameStarted": True})


def test_json_call(request):
    """Used to test a vertical slice of the stack."""
    print(request)
    if request.is_ajax() and request.method == 'POST':
        print(request.body)
        data = request.POST.get("userInput", "")
        user_id = request.session["user_id"]
        print("User from %s submitted %s" % (user_id, data))
    return JsonResponse({"direction": "North", "distance": 10})
