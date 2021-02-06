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
            $("#terminalOutputBox").append(data.terminalLine + "<br>")
            $('#terminalOutputBox').animate({scrollTop: $('#terminalOutputBox').prop("scrollHeight")}, 10);
        } else {
            console.log("ERROR: failed to post user input")
        }
    })
    $('#userTextInput').val("")
}

$('#userTextInput').on('keypress', function (e) {
    if(e.which == 13) {
        submitUserInput()
    }
});
