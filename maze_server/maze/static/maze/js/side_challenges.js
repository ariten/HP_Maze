$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});
})

function submitAnswer(question_num) {
    userInput = $('#userTextInputSC' + question_num).val()

    $.post(
        "/submitsidechallenge",
        {
            "userInput": userInput,
            "question": question_num,
        },
        function (data) {
            $('#scResult' + question_num).html(data)
        }
    )
}
