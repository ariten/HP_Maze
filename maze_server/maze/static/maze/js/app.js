$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});
})

function submitUserInput() {
    const userInput = $("#userTextInput").val()
    console.log("Input: " + userInput)
    $.post("/userinput", {"userInput": userInput}, function (data) {
        if (data.success) {
            $("#terminalOutputBox").append("<br>" + data.terminalLine)
            $('#terminalOutputBox').animate({scrollTop: $('#terminalOutputBox').prop("scrollHeight")}, 10);

            // Handle lockout if user got a question wrong
            if (data.lockout) {
                console.log("Locking terminal for " + data.lockoutDuration + " seconds")
                lockoutTerminal(data.lockoutDuration)
            }
        } else {
            console.log("ERROR: failed to post user input")
        }
    })
    $('#userTextInput').val("")
}

function lockoutTerminal(duration) {
    $('#userTextInput').prop("disabled", true)
    $('#terminalBottomBar').css("background-color", "#791212")
    setTimeout(function () {
        $('#userTextInput').prop("disabled", false)
        $('#userTextInput').focus()
        $('#terminalBottomBar').css("background-color", "#4d4d4d")
    }, duration * 1000)
}

$('#userTextInput').on('keypress', function (e) {
    if(e.which == 13) {
        submitUserInput()
    }
});
