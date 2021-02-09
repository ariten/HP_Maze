import json
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import GameStart, Team
from maze_handler.MazeHandler import MazeHandler
from side_challenge_handler.SideHandler import SideHandler

DEBUG = True

MAZE_HANDLER = MazeHandler(nx=10, ny=10, load_maze_file='Friday_maze.mz')
SIDE_HANDLER = SideHandler()

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


def page_side_challenges(request):
    """Show the user a page of side challenges."""
    # Check to see if the user has selected a team yet, if not redirect to the selection page
    if "user_id" not in request.session:
        return redirect('team_selection')
    
    user_id = request.session["user_id"]
    return render(request, 'maze/side_challenges.html', {"user_id": user_id})


def api_register_team(request):
    """Takes the user's input of team name and stores it in the session as the user's unique ID."""
    if request.is_ajax() and request.method == 'POST':
        team_name = request.POST.get("userSelection", "")
        print("User selected team %s" % team_name)
        request.session["user_id"] = team_name

        # Register the team with the maze handler
        MAZE_HANDLER.register_team(team_name)

        return JsonResponse({"success": True, "teamName": request.session["user_id"]})
    return JsonResponse({"success": False})


def api_user_input(request):
    """Process a command line command sent by the user."""
    user_id = request.session["user_id"]
    if request.is_ajax() and request.method == 'POST':
        user_input = request.POST.get("userInput", "")
        print("User from %s submitted %s" % (user_id, user_input))

        team = Team.objects.get(team_name=user_id)
        print(team)

        if not DEBUG:
            game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
            if datetime.now() < game_start_time:
                return JsonResponse({
                    "success": True,
                    "terminalLine": "The game has not started yet.",
                    "lockout": False,
                    "lockoutDuration": 0,
                    "score": 0,
            })

            game_end_time = game_start_time + timedelta(minutes=15)
            if datetime.now() > game_end_time:
                return JsonResponse({
                    "success": True,
                    "terminalLine": "You are too late, the game has ended.",
                    "lockout": False,
                    "lockoutDuration": 0,
                    "score": team.score,
            })

            # Check to see if the user is leaving early, and block if time is too close to end of game
            if user_input.lower() == "periculum":
                game_end_time = game_start_time + timedelta(minutes=13, seconds=30)
                if datetime.now() > game_end_time:
                    return JsonResponse({
                        "success": True,
                        "terminalLine": "It is too late to escape with the Periculum spell, you will need to find the exit.",
                        "lockout": False,
                        "lockoutDuration": 0,
                        "score": team.score,
                })


        # Pass the user input to the maze code and get back assorted info
        results = MAZE_HANDLER.process_input(user_id, user_input)
        print("--- RESULTS ---")
        print(results)
        print("--- END OF RESULTS ---")
        output = results["info"]
        score_change = results["score"]
        duration = results["timeout"]
        lockout = duration != 0
        print("SCORE CHANGE: " + str(score_change))

        # Update the team score based on the returned delta
        if score_change > 0 and score_change < 1:
            team.score = int(team.score * score_change)
            team.save()
        if score_change >= 1 or score_change < 0:
            team.score += score_change
            team.save()

        reply_data = {
            "success": True,
            "terminalLine": output,
            "lockout": lockout,
            "lockoutDuration": duration,
            "score": team.score,
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

        # Calculate seconds left on the 15 min timer
        timer_remaining = max(int((timedelta(minutes=15) + time_remaining).total_seconds()), 0)

        if delta > 0:
            return JsonResponse({"gameStarted": False, "duration": delta})
        else:
            return JsonResponse({"gameStarted": True, "duration": timer_remaining})


def api_submit_side_challenge(request):
    """Check to see if the submitted answer is correct, and update the team's score if it is."""
    if request.is_ajax() and request.method == 'POST':
        user_input = request.POST.get("userInput", "")
        question_num = int(request.POST.get("question", "0"))
        user_id = request.session["user_id"]

        stuff = SIDE_HANDLER.handle(question_num, user_input, user_id)
        print(stuff)
        correct, image_name, score_change = stuff
        
        if correct == "Success":
            # Update the team's score if the change is not zero
            # Score stuff

            return render(request, 'maze/sc_success.html', {"image_path": 'maze/img/' + image_name, "user_input": user_input})
        else:
            print("Returning failure template")
            test = render(request, 'maze/sc_failure.html', {"user_input": user_input})
            print(test)
            return test




def test_json_call(request):
    """Used to test a vertical slice of the stack."""
    print(request)
    if request.is_ajax() and request.method == 'POST':
        print(request.body)
        data = request.POST.get("userInput", "")
        user_id = request.session["user_id"]
        print("User from %s submitted %s" % (user_id, data))
    return JsonResponse({"direction": "North", "distance": 10})
