
class MinimaxSearch {
    // score = (x => 1)
    // getNextMoves = (x => x)
    /**
     * Store a game model into the object
     * @param {function} scoreFunc A scoring function that scores higher for
     * states that favor one player and lower for those that favor the other. It
     * should return a number or null if it only evaluates an end state
     * @param {function} getNextMovesFunc A function that returns an array of
     * the next possible states based off the current one
     */
    constructor(scoreFunc, getNextMovesFunc) {
        this.bestMove = null
        // this.score = scoreFunc
        // this.getNextMoves = getNextMovesFunc
    }

    // set score(func) { this.score = func }
    // set getNextMoves(func) { this.getNextMoves = func }

    /**
     * 
     * @param {*} state 
     * @param {number, null} maxDepth pass null if the scoring function returns
     * null for all states other than the end
     */
    search(state, maxDepth = null) {
        if (maxDepth === null) {
            
        } else {
            // im not doing this rn
        }
    }

    minStep(state, depth=0) {
        // if (depth > 20) return
        // console.log("minStep: ", state.state)
        let score = state.score()
        if (score != null) {
            // console.log("returning score: ", score)
            return score
        }
        else {
            let bestMove = null
            let minScore = Infinity
            let nextMoves = state.getNextMoves()
            console.log("\t"*depth + "nextMoves: ", nextMoves)
            for (let i=0; i < nextMoves.length; i++) {
                let newState = state.clone()
                // console.log("newState: ", newState.state)
                newState.makeMove(nextMoves[i])
                // console.log("newStat2e: ", newState.state)
                let score = this.maxStep(newState, depth+1)
                if (score < minScore) {
                    minScore = score
                    bestMove = nextMoves[i]
                    this.bestMove = nextMoves[i]
                }
            }
            return minScore
        }
    }

    maxStep(state, depth=0) {
        // if (depth > 20) return
        // console.log("maxStep: ", state.state)
        let score = state.score()
        if (score != null)
            return score
        else {
            let bestMove = null
            let maxScore = -Infinity
            let nextMoves = state.getNextMoves()
            for (let i=0; i < nextMoves.length; i++) {
                let newState = state.clone()
                newState.makeMove(nextMoves[i])
                let score = this.minStep(newState, depth+1)
                if (score > maxScore) {
                    maxScore = score
                    bestMove = nextMoves[i]
                    this.bestMove = nextMoves[i]
                }
            }
            return maxScore
        }
    }
}

export {MinimaxSearch}