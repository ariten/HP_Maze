$(document).ready(function(){
    // Get the CSRF token and set it in the AJAX headers for later $.post calls
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajaxSetup({headers: { 'X-CSRFToken': csrftoken }});

})

function submitSelectedTeam() {
    var selectedTeamName = $("#teamSelectDropdown").val()
    console.log(selectedTeamName)
    $.post(
        "/registerteam",
        {"userSelection": selectedTeamName},
        function (data) {
            console.log(data)
            if (data.success == true) {
                console.log("User selected team " + data.teamName)
                window.location.replace("/")
            }
        }
    )
}
