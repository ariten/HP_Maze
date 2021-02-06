$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});


    // Get the user's team name (used as a unique ID) and send it to the django server
    var userTeamInput = prompt("What team are you on?")
    $.post(
        "/registerteam",
        {"userInput": userTeamInput},
        function (data) {
            console.log(data)
            if (data.success == true) {
                console.log("User registered as team " + data.teamName)
            }
        }
    )
})

function submitUserInput() {
    const userInput = $("#userTextInput").val()
    console.log(userInput)
    $.post("/testjson", {"userInput": userInput}, function (data) {
        console.log(data)
    })
}
