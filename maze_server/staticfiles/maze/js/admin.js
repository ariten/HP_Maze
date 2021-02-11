

function endGame() {

    if (confirm("Are you sure you want to end the game?")) {
        $.getJSON(
            '/adminendgame',
            function (data) {
                if (data.success) {
                    alert("Game ended successfully, " + data.numTrapped + " teams have been trapped in the maze.")
                    location.reload()
                } else {
                    alert("Error! End game API endpoint failed.")
                }
            }
        )
    }    
}
