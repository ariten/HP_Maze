$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});
})

function submitUserInput() {
    const userInput = $("#userTextInput").val()
    console.log(userInput)
    $.post("/testjson", {"userInput": userInput}, function (data) {
        console.log(data)
    })
}
