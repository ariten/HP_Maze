$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});

    // Check to see if the game has started, if it has not, lock out the terminal for the remaining time
    $.getJSON(
        "/timeuntilstart",
        function (data) {
            if (!data.gameStarted) {
                console.log("Game starts in " + data.duration + " seconds, locking terminal")
                lockoutTerminal(data.duration)
            }
        }
    )
})

function submitUserInput() {
    const userInput = $("#userTextInput").val()
    console.log("Input: " + userInput)
    $("#terminalOutputBox").append("<br>> " + userInput)
    $.post("/userinput", {"userInput": userInput}, function (data) {
        if (data.success) {
            $("#terminalOutputBox").append("<br>" + data.terminalLine)
            $('#terminalOutputBox').animate({scrollTop: $('#terminalOutputBox').prop("scrollHeight")}, 10);
            $('#scoreBox').text("Score: " + data.score)

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
    $('#lockoutOverlay').css("visibility", "visible")
    $('#terminalBottomBar').css("background-color", "#791212")
    display = document.querySelector('#lockoutTimer');
    startTimer(duration, display)
    setTimeout(function () {
        $('#userTextInput').prop("disabled", false)
        $('#userTextInput').focus()
        $('#terminalBottomBar').css("background-color", "#4d4d4d")
        $('#lockoutOverlay').css("visibility", "hidden")
    }, duration * 1000)
}

// Timer taken from https://stackoverflow.com/questions/20618355/the-simplest-possible-javascript-countdown-timer
function startTimer(duration, display) {
    var start = Date.now(),
        diff,
        minutes,
        seconds;
    function timer() {
        // get the number of seconds that have elapsed since 
        // startTimer() was called
        diff = duration - (((Date.now() - start) / 1000) | 0);

        // does the same job as parseInt truncates the float
        minutes = (diff / 60) | 0;
        seconds = (diff % 60) | 0;

        if (minutes == 0 && seconds == 0) {
            clearInterval(x)
        }

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;
    };
    // we don't want to wait a full second before the timer starts
    timer();
    x = setInterval(timer, 1000);
}

$('#userTextInput').on('keypress', function (e) {
    if(e.which == 13) {
        submitUserInput()
    }
});
