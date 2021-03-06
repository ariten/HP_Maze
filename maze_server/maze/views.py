import json
from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import GameStart, Team
from maze_handler.MazeHandler import MazeHandler
from side_challenge_handler.SideHandler import SideHandler
from django.templatetags.static import static

DEBUG = False

MAZE_HANDLER = MazeHandler(nx=10, ny=10, load_maze_file='Friday_maze.mz')
SIDE_HANDLER = SideHandler()


def index(request):
    """The page the user sees when they load the site."""
    # Check to see if the user has selected a team yet, if not redirect to the selection page
    if "user_id" not in request.session:
        return redirect('team_selection')

    user_id = request.session["user_id"]
    team = Team.objects.get(team_name=user_id)
    return render(request, "maze/index.html", {"user_id": user_id,  "score": team.score})


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
    team = Team.objects.get(team_name=user_id)
    game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
    game_end_time = game_start_time + timedelta(minutes=GameStart.objects.first().event_duration)
    if datetime.now() < game_start_time or datetime.now() > game_end_time:
        reply_data = {
            "user_id": user_id,
            "score": team.score,
            "q1": "???",
            "q2": "???",
            "q3": "???",
            "q4": "???",
            "q4a": "???"
        }
    else:
        reply_data = {
            "user_id": user_id,
            "score": team.score,
            "q1": "fvevhf oynpx",
            "q2": "01100101 01110010 01110010 01101111 01101100",
            "q3": "yyntnabtpz",
            "q4": "cuieyqgecfoy",
            "q4a": "Now this one is a hard one, the key is located near one of the horcrux's",
        }
    return render(request, 'maze/side_challenges.html', reply_data)


def page_admin_extras(request):
    """Return a few extra admin things."""
    if request.user.is_staff:
        all_teams = Team.objects.values()
        side_challenges = SIDE_HANDLER.get_stats()
        questions_answered = MAZE_HANDLER.get_stats()

        for team in all_teams:
            # Add questions answered to team data
            if team["team_name"] in questions_answered.keys():
                team["questions"] = questions_answered[team["team_name"]]
            else:
                team["questions"] = "TNR"

            # Add side challenges completed to team data
            if team["team_name"] in side_challenges.keys():
                team["sides"] = side_challenges[team["team_name"]]
            else:
                team["sides"] = "TNR"

        print(all_teams)

        context = {"teams": all_teams}
        return render(request, 'maze/page_admin.html', context)
    else:
        return HttpResponse(status=401)


def api_admin_end_game(request):
    if request.user.is_staff:
        if request.is_ajax() and request.method == 'GET':
            # End the game by getting the trapped teams and halving their scores
            trapped_teams = MAZE_HANDLER.game_over()
            for team_name in trapped_teams:
                team = Team.objects.get(team_name=team_name)
                team.score = int(team.score / 2)
                team.save()

            return JsonResponse({"success": True, "numTrapped": len(trapped_teams)})
    else:
        return HttpResponse(status=401)

def api_admin_reset_game(request):
    if request.user.is_staff:
        if request.is_ajax() and request.method == 'GET':
            global MAZE_HANDLER
            MAZE_HANDLER = MazeHandler(nx=10, ny=10, load_maze_file='Friday_maze.mz')
            return JsonResponse({"success": True})
    else:
        return HttpResponse(status=401)

def api_register_team(request):
    """Takes the user's input of team name and stores it in the session as the user's unique ID."""
    if request.is_ajax() and request.method == 'POST':
        team_name = request.POST.get("userSelection", "")
        print("User selected team %s" % team_name)
        request.session["user_id"] = team_name

        # Register the team with the maze handler
        MAZE_HANDLER.register_team(team_name)
        SIDE_HANDLER.register_team(team_name)

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

            game_end_time = game_start_time + timedelta(minutes=GameStart.objects.first().event_duration)
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
                game_end_time = game_start_time + (timedelta(minutes=GameStart.objects.first().event_duration) -
                                                   timedelta(minutes=5))
                if datetime.now() > game_end_time:
                    return JsonResponse({
                        "success": True,
                        "terminalLine": "It is too late to escape with the Periculum spell, you will need to find the "
                                        "exit.",
                        "lockout": False,
                        "lockoutDuration": 0,
                        "score": team.score
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
        if output == "You have used a spell to escape!" or output == "You have safely escaped the maze!":
            SIDE_HANDLER.add_exit(user_id)
        print("SCORE CHANGE: " + str(score_change))

        # Update the team score based on the returned delta
        if 0 < score_change < 1:
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
        timer_remaining = max(int((timedelta(minutes=GameStart.objects.first().event_duration) + time_remaining).total_seconds()), 0)

        if delta > 0:
            return JsonResponse({"gameStarted": False, "duration": delta})
        else:
            user_id = request.session["user_id"]
            message = MAZE_HANDLER.get_start_options(user_id)
            return JsonResponse({"gameStarted": True, "duration": timer_remaining, "message": message})


def api_get_game_start_info(request):
    """Return the initial game message and time remaining in the game."""
    if request.is_ajax() and request.method == 'GET':
        game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
        time_remaining = game_start_time - datetime.now()
        timer_remaining = max(int((timedelta(minutes=GameStart.objects.first().event_duration) + time_remaining).total_seconds()), 0)

        user_id = request.session["user_id"]
        message = MAZE_HANDLER.get_start_options(user_id)

        return JsonResponse({"message": message, "duration": timer_remaining})


def api_submit_side_challenge(request):
    """Check to see if the submitted answer is correct, and update the team's score if it is."""
    if request.is_ajax() and request.method == 'POST':
        user_input = request.POST.get("userInput", "")
        question_num = int(request.POST.get("question", "0"))
        user_id = request.session["user_id"]

        stuff = SIDE_HANDLER.handle(question_num, user_input, user_id)
        print(stuff)
        correct, image_name, score_change = stuff

        team = Team.objects.get(team_name=user_id)
        game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
        game_end_time = game_start_time + timedelta(minutes=GameStart.objects.first().event_duration)

        if datetime.now() < game_start_time:
            message = "The event has not started, event starts in %s." % str(game_start_time - datetime.now()).split(".")[0]
            reply_data = {
                "correct": False,
                "message": message,
                "score": team.score,
            }
        elif datetime.now() > game_end_time:
            message = "The event has ended."
            reply_data = {
                "correct": False,
                "message": message,
                "score": team.score,
            }
        else:
            if correct == "ERROR":
                reply_data = {
                    "correct": False,
                    "message": "You have already exited the Maze",
                    "score": team.score
                }
            elif correct == "Success":
                # Update the team's score if the change is not zero
                # Score stuff
                team.score += score_change
                team.save()

                if score_change == 0:
                    message = "You have already answered Question %s." % question_num
                else:
                    message = '"%s" was the correct answer, %s score has been added to your team.' % (user_input, score_change)

                image_path = static('maze/img/' + image_name)
                print(image_path)

                reply_data = {
                    "correct": True,
                    "message": message,
                    "imagePath": image_path,
                    "score": team.score,
                }
            else:
                message = '"%s" was the wrong answer, sorry.' % user_input

                reply_data = {
                    "correct": False,
                    "message": message,
                    "score": team.score,
                }

        return JsonResponse(reply_data)


def api_get_hint(request):
    user_id = request.session["user_id"]
    if request.is_ajax() and request.method == 'POST':
        game_start_time = GameStart.objects.first().start_time.replace(tzinfo=None)
        game_end_time = game_start_time + timedelta(minutes=GameStart.objects.first().event_duration)

        if datetime.now() < game_start_time:
            message = "The event has not started, event starts in %s." % \
                      str(game_start_time - datetime.now()).split(".")[0]
            reply_data = {
                "message": message,
            }
        elif datetime.now() > game_end_time:
            message = "The event has ended."
            reply_data = {
                "message": message,
            }
        else:
            question_num = int(request.POST.get("question", "0"))
            hint = SIDE_HANDLER.hint_handler(question=question_num, team=user_id)
            reply_data = {
                "message": hint
            }
        return JsonResponse(reply_data)


def test_json_call(request):
    """Used to test a vertical slice of the stack."""
    print(request)
    if request.is_ajax() and request.method == 'POST':
        print(request.body)
        data = request.POST.get("userInput", "")
        user_id = request.session["user_id"]
        print("User from %s submitted %s" % (user_id, data))
    return JsonResponse({"direction": "North", "distance": 10})
