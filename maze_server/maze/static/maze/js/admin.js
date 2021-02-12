

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

function reset() {
    if (confirm("Are you sure you want to reset the game?")) {
        $.getJSON(
            '/adminresetgame',
            function (data) {
                if (data.success) {
                    alert("Game reset successfully")
                    location.reload()
                } else {
                    alert("Error! End game API endpoint failed.")
                }
            }
        )
    }
}
