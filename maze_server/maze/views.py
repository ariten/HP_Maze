import json
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    """The page the user sees when they load the site."""
    return render(request, "maze/index.html")


def test_json_call(request):
    """Used to test a vertical slice of the stack."""
    print(request)
    if request.is_ajax() and request.method == 'POST':
        print(request.body)
        data = request.POST.get("userInput", "")
        print(data)
    return JsonResponse({"direction": "North", "distance": 10})
