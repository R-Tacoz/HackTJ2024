import { TicTacToe } from "./tictactoe.js"

let cells = document.querySelectorAll('#game_area .board_cell')
let resetButton = document.getElementById('reset_button')
let gameDisplay = document.getElementById('game_ending_display')

cells.forEach(cell => cell.addEventListener('click', onCellClick))
resetButton.addEventListener('click', resetGame)

const HIGHLIGHT = "#00FF00A0"
const TOKEN_SRC = new Map([
    [TicTacToe._X, "./static/res/red_x.svg"],
    [TicTacToe._O, "./static/res/black_o.svg"]])
let game = new TicTacToe()

function onCellClick() {
    if (game.winner != TicTacToe._NONE) return
    

    let madeMove = game.makeMove(parseInt(this.dataset.cell_id))
    if (madeMove) {
        this.innerHTML = "<object data="+TOKEN_SRC.get(-game.currentPlayer)+"></object>"

        // console.log("bestMove: ", game.AIMove)
        switch (game.winner) {
            case TicTacToe._NONE:
                gameDisplay.innerHTML = TicTacToe.TOKEN_MAP.get(game.currentPlayer)+"'s Turn"
                break
            case TicTacToe._TIE:
                gameDisplay.innerHTML = "It's a tie!"
                break
            case TicTacToe._X:
            case TicTacToe._O:
                gameDisplay.innerHTML = `${TicTacToe.TOKEN_MAP.get(game.winner)} wins!`
                
                for (let i=0; i < game.winLine.length; i++)
                    cells[game.winLine[i]].style['background-color'] = HIGHLIGHT
                break
        }
    }
    
}

function resetGame() {
    game.reset()
    for (let i=0; i < cells.length; i++) {
        cells[i].innerHTML = ""
        cells[i].style['background-color'] = "white"
    }
    gameDisplay.innerHTML = "X's Turn."
}