# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    
        foodDist = min([manhattanDistance(newPos, food) for food in newFood.asList()] + [500])
        ghostDist = min([manhattanDistance(newPos, ghost) for ghost in newGhostPos])
        if ghostDist < 2:
            ghostValue = -500
        else:
            ghostValue = 0
        value = successorGameState.getScore() + 5.0 / (foodDist+1) + ghostValue
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        children = [gameState.generateSuccessor(0, action) for action in gameState.getLegalActions(0)]
        scores = [self.minValue(child, 1, 1) for child in children]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return gameState.getLegalActions()[chosenIndex]
        
        
    def maxValue(self, gs, currDepth):
        if currDepth == self.depth:
            return self.evaluationFunction(gs)
        children = [gs.generateSuccessor(0, action) for action in gs.getLegalActions(0)]
        if not children:
            return self.evaluationFunction(gs)
        return max([self.minValue(child, currDepth+1, 1) for child in children])
            
    def minValue(self, gs, currDepth, agentIndex):
        if agentIndex == gs.getNumAgents():
            return self.maxValue(gs, currDepth)
        children = [gs.generateSuccessor(agentIndex, action) for action in gs.getLegalActions(agentIndex)]
        if not children:
            return self.evaluationFunction(gs)
        return min([self.minValue(child, currDepth, agentIndex+1) for child in children])
        
        
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        a = float('-inf')
        b = float('inf')
        v = float('-inf')
        actions = gameState.getLegalActions(0)
        for action in actions:
            currVal = self.minValue(gameState.generateSuccessor(0, action), a, b, 1, 1)
            if currVal > v:
                v = currVal
                bestAction = action
            a = max(a, v)
        return bestAction
    
    
    
    
    def maxValue(self, gs, a, b, currDepth):
        if currDepth == self.depth:
            return self.evaluationFunction(gs)
        v = float('-inf')
        actions = gs.getLegalActions(0)
        if not actions:
            return self.evaluationFunction(gs)
        for action in actions:
            v = max(v, self.minValue(gs.generateSuccessor(0, action), a, b, currDepth+1, 1))
            if v > b:
                return v
            a = max(a, v)
        return v
        
    def minValue(self, gs, a, b, currDepth, agentIndex):
        if agentIndex == gs.getNumAgents():
            return self.maxValue(gs, a, b, currDepth)
        v = float('inf')
        actions = gs.getLegalActions(agentIndex)
        if not actions:
            return self.evaluationFunction(gs)
        for action in actions:
            v = min(v, self.minValue(gs.generateSuccessor(agentIndex, action), a, b, currDepth, agentIndex+1))
            if v < a:
                return v
            b = min(b, v)
        return v    

        
        
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        children = [gameState.generateSuccessor(0, action) for action in gameState.getLegalActions(0)]
        scores = [self.expectiValue(child, 1, 1) for child in children]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)
        return gameState.getLegalActions()[chosenIndex]
        
        
    def maxValue(self, gs, currDepth):
        if currDepth == self.depth:
            return self.evaluationFunction(gs)
        children = [gs.generateSuccessor(0, action) for action in gs.getLegalActions(0)]
        if not children:
            return self.evaluationFunction(gs)
        return max([self.expectiValue(child, currDepth+1, 1) for child in children])
            
    def expectiValue(self, gs, currDepth, agentIndex):
        if agentIndex == gs.getNumAgents():
            return self.maxValue(gs, currDepth)
        children = [gs.generateSuccessor(agentIndex, action) for action in gs.getLegalActions(agentIndex)]
        if not children:
            return self.evaluationFunction(gs)
        return float(sum([self.expectiValue(child, currDepth, agentIndex+1) for child in children])) / len(children)
    

    
    
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    
        foodDist = min([manhattanDistance(newPos, food) for food in newFood.asList()] + [500])
        ghostDist = min([manhattanDistance(newPos, ghost) for ghost in newGhostPos])
        if ghostDist < 2:
            ghostValue = -500
        else:
            ghostValue = 0
        value = successorGameState.getScore() + 5.0 / (foodDist+1) + ghostValue
        return value
    """  
        
    gs = currentGameState
    pos = gs.getPacmanPosition()
    foods = gs.getFood()
    score = gs.getScore()
    ghosts = gs.getGhostStates()
    ghostPosts = gs.getGhostPositions()
    scaredTimes = [ghost.scaredTimer for ghost in ghosts]
    ghostDist = min([manhattanDistance(pos, ghost) for ghost in ghostPosts])
    foodDist = min([manhattanDistance(pos, food) for food in foods.asList()] + [500])
    
    if min(scaredTimes) > ghostDist:
        ghostValue = 200 / (ghostDist+1)
    elif ghostDist < 2:
        ghostValue = -100
    else:
        ghostValue = 0
    
    return score + 5.0 / (foodDist+1) + ghostValue
        
        

# Abbreviation
better = betterEvaluationFunction

