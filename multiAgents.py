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
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"
		return successorGameState.getScore()

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
		"""
		"*** YOUR CODE HERE ***"
		#Start the iteration
		bestValue, bestAction = self.maxValue(gameState, self.depth)
		return bestAction
		
		#Make two recursive functions, one for maxValue, and one for
		#	minValue.
		#Start these from the function and keep track of the depth by
		#	starting it as self.depth and decrease each recursion when
		#	you have checked moves for the last ghost
		
	#MaxValue is called for Pacman's turn and return the highest
	#	of the minvalues along with the action
	def maxValue(self, gameState, depth):
		#Check if it's as deep as it gets, if not return the highest
		#	value from the possible moves. Also check if the game is
		#	over
		if depth == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState), "noMove"
		else:
			#When running max, the agent is allways Pacman
			legalActions = gameState.getLegalActions()
			value =  -(float("inf"))
			for action in legalActions:
				#After Pacman (0), the next agent is ghost nr. 1
				tempValue = self.minValue(gameState.generateSuccessor(0, action), depth, 1)
				if tempValue > value:
					value = tempValue
					bestAction = action
			return value, bestAction
		
	#MinValue is called for the ghost's turn and return the smallest
	#	value for the turns.
	def minValue(self, gameState, depth, agentIndex):
		if depth == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		else:
			value = float("inf")
			legalActions = gameState.getLegalActions(agentIndex)
			#If it's the last ghost then take the lowest value of
			#	the different actions put into the maxValue-function
			#	as it's Pacman's turn next. Also decrease depth.
			#	If not then take the lowest value of the different
			#	actions put into the minValue with agentIndex += 1,
			#	as a ghost is up next. Don't decrease depth, but
			#	increase agentIndex.
			if agentIndex == (gameState.getNumAgents() - 1):
				for action in legalActions:
					tempValue, trash = self.maxValue(gameState.generateSuccessor(agentIndex, action), (depth - 1))
					if tempValue < value:
						value = tempValue
			else:
				for action in legalActions:
					tempValue = self.minValue(gameState.generateSuccessor(agentIndex, action), depth, (agentIndex + 1))
					if tempValue < value:
						value = tempValue
			return value

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		#Copy paste the code from miniMaxAgent and extend them
		#	to use alpha- and beta values.
		#Start with alpha and beta as their worst. Use one beta
		#	for all ghosts.
		#Start iteration in getAction to ease availability of
		#	action
		alpha = -(float("inf"))
		beta = (float("inf"))
		legalActions = gameState.getLegalActions()
		bestAction = legalActions[0]
		value =  -(float("inf"))
		for action in legalActions:
			tempValue = self.minValue(gameState.generateSuccessor(0, action), self.depth, 1, alpha, beta)
			#v = max(v, tempValue)
			if tempValue > value:
				value = tempValue
				bestAction = action
			#If v>beta return v
			if value > beta:
				return tempValue
			#alpha = max(apha,v)
			if value > alpha:
				alpha = value
		return bestAction
		
	def maxValue(self, gameState, depth, alpha, beta):
		if depth == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		else:
			legalActions = gameState.getLegalActions()
			value =  -(float("inf"))
			for action in legalActions:
				tempValue = self.minValue(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
				#v = max(v, tempValue)
				if tempValue > value:
					value = tempValue
					bestAction = action
				#If v>beta return v
				if value > beta:
					return value
				#alpha = max(apha,v)
				if value > alpha:
					alpha = value
			return value
		
	def minValue(self, gameState, depth, agentIndex, alpha, beta):
		if depth == 0 or gameState.isWin() or gameState.isLose():
			return self.evaluationFunction(gameState)
		else:
			value = float("inf")
			legalActions = gameState.getLegalActions(agentIndex)
			if agentIndex == (gameState.getNumAgents() - 1):
				for action in legalActions:
					tempValue = self.maxValue(gameState.generateSuccessor(agentIndex, action), (depth - 1), alpha, beta)
					#v = min(v,temp)
					if tempValue < value:
						value = tempValue
					#If v<alpha return value
					if value < alpha:
						return value
					#beta = min(beta,v)
					if value < beta:
						beta = value
			else:
				for action in legalActions:
					tempValue = self.minValue(gameState.generateSuccessor(agentIndex, action), depth, (agentIndex + 1), alpha, beta)
					#v = min(v,temp)
					if tempValue < value:
						value = tempValue
					#If v<alpha return value
					if value < alpha:
						return value
					#beta = min(beta,v)
					if value < beta:
						beta = value
			return value

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
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

