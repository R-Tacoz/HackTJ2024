// import { MinimaxSearch } from "{{url_for('static', filename='./scripts/minimax.js')}}"

class TicTacToe {
    // these vars represent both the token, the player, and the winner
    static _X = 1
    static _O = -1
    static _NONE = 0
    static _TIE = 2

    static TOKEN_MAP = new Map([
        [TicTacToe._X, 'X'], 
        [TicTacToe._O, 'O']
    ])
    static WINDICES = [
        [0,1,2], [3,4,5], [6,7,8], [0,3,6], 
        [1,4,7], [2,5,8], [0,4,8], [2,4,6]
    ]

    #state
    #numEmptyCells
    #AI
    currentPlayer = TicTacToe._X
    winner = TicTacToe._NONE
    winLine = null
    constructor() { 
        this.reset()
        // this.#AI = new MinimaxSearch(this.checkState, TicTacToe.getNextMoves)
    }

    /**
     * If possible, make a move and switch turns
     * @param {number} cellId 0-9
     * @returns {boolean} if the move was made
     */
    makeMove(cellId) {
        // if the game has ended or the cell in question is already full
        // console.log("making move: ", cellId)
        // console.log("cur winner: ", this.winner)
        if (this.winner != TicTacToe._NONE || 
            this.#state[cellId != TicTacToe._NONE]) 
            return false 

        this.#state[cellId] = this.currentPlayer
        this.#numEmptyCells--
        this.currentPlayer *= -1
        this.winner = this.checkState()
        return true
    }

    /**
     * Calculates the current winner of the game 
     * @returns _X, _O, _TIE, or _NONE
     */
    checkState() {
        // optimization: game cannot end in less than 5 moves
        if (this.#numEmptyCells >= 5)
            return TicTacToe._NONE
        // iterate through all possible 3-in-a-rows
        windicesLoop: for (let i=0; i < TicTacToe.WINDICES.length; i++) 
        {
            let line = TicTacToe.WINDICES[i]

            // check the 3-in-a-row, if it fails, go to next in-a-row
            let first = this.#state[line[0]]
            if (first == TicTacToe._NONE) 
                continue windicesLoop
            for (let j=1; j < line.length; j++) 
            {
                let token = this.#state[line[j]]
                if (token != first) 
                    continue windicesLoop
            }
            // the 3-in-a-row was filled; return winner
            this.winLine = line
            return first
        }
        // no 3-in-a-rows were filled; return no winner or tie
        return (this.#numEmptyCells == 0) ? TicTacToe._TIE : TicTacToe._NONE
    }

    score() {
        let score = this.checkState()
        if (score == TicTacToe._NONE) return null
        else return score
    }

    reset() {
        this.#state = new Array(9).fill(TicTacToe._NONE)
        this.#numEmptyCells = this.#state.length
        this.currentPlayer = TicTacToe._X
        this.winner = TicTacToe._NONE
        this.winLine = null
    }

    clone() {
        let copy = new TicTacToe()
        copy.#state = structuredClone(this.#state)
        copy.#numEmptyCells = this.#numEmptyCells
        copy.currentPlayer = this.currentPlayer
        copy.winner = this.winner
        copy.winLine = this.winLine
        return copy
    }

    /**
     * Returns a list of all next moves, AKA all the empty cells. Moves do not
     * include the player since it can be tracked during the search.
     * @param {Array<number>} state 
     * @param {boolean} player True if it's X's turn, false otherwise
     */
    getNextMoves(player) {
        let moves = new Array()
        for (let i=0; i < this.#state.length; i++)
            if (this.#state[i] == TicTacToe._NONE)
                moves.push(i)
        return moves
    }

    /**
     * Uses the minimax search algorithm to select the current best
     * move
     * @returns the move as a cell ID
     */
    get AIMove() {
        let bestMove = this.#AI.maxStep(this.clone())
        return this.#AI.bestMove
    }

    get state() { return this.#state }
    get numEmptyCells() { return this.#numEmptyCells }

}

export { TicTacToe }