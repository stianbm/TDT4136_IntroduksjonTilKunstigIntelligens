#Needed to read from the file
from sys import stdin


#Define the datastructrure of SearchNode, state is given as x- and y coordinates
class SearchNode:
	def __init__(self, Row, Col, Board):
		self.row = Row
		self.col = Col
		self.g = 0
		self.h = 0
		self.f = 0
		self.parent = None
		self.kids = []
		letter = Board[Row][Col]
		if letter == 'w':
			self.cost = 100
		elif letter == 'm':
			self.cost = 50
		elif letter == 'f':
			self.cost = 10
		elif letter == 'g':
			self.cost = 5
		else:
			self.cost = 1
		
		
#Print node
def PrintNode(X):
	print("-----------------------")
	print(X.row)
	print(X.col)
	print(X.g)
	print(X.h)
	print(X.f)
	print(X.parent)
	print(X.kids)
	print(X.cost)
	print("-----------------------")

	
#Compute Manhattan distance / h from row and col to "B"
def FindDistance(Rowi, Coli, B):
	DistX = Rowi - B[0]
	DistY = Coli - B[1]
	return abs(DistX) + abs(DistY)
		
	
#Give the node its apropriate values
def InitiateNode(X, BoardB, Parent, Created, ParentG):
	X.h = FindDistance(X.row, X.col, BoardB)
	X.g = ParentG + X.cost
	X.f = X.g + X.h
	Created[X.row][X.col] = X
	return X
	
		
#Print the variable "Board"
def Print(Board):
	Row = len(Board[0])
	for line in Board:
		for i in range(0,Row-1):
			print(line[i], end="")
		print("")
		
	
#Updates teh Board
def UpdateBoard(X, Board):
	while X.parent != None:
		X = X.parent
		if Board[X.row][X.col] != 'A':
			Board[X.row][X.col] = 'O'
	return Board
	
	
#Generate the children if they don't fall outside the board
def GenerateSuccessors(X, MaxRow, MaxCol, BoardB, Board, Created):
	SUCC = []
	Child = None
	x = X.row
	y = X.col
	Iterator = [(x-1, y), (x+1,y), (x, y-1), (x, y+1)]
	for x_,y_ in Iterator:
		if 0 <= x_ < MaxRow and 0 <= y_ < MaxCol:
			if Board[x_][y_] != '#':
				Child = SearchNode(x_, y_, Board)
				Child = InitiateNode(Child, BoardB, X, Created, X.g)
				SUCC.append(Child)
	return SUCC
	
	
#Check if node has been created, if so, return the previously created node. Keep track with matrix of
#	created nodes
def PreviouslyCreated(node, Created):
	if Created[node.row][node.col] != None:
		return Created[node.row][node.col]
	else:
		return node
	
	
#Check if "S" is in CLOSED	
def InCLOSED(S, CLOSED):
	for node in CLOSED:
		if node == 0:
			return False
		if node.row == S.row and node.col == S.col:
			return True
	return False

	
#Check if "S" is in OPEN
def InOPEN(S, OPEN):
	for node in OPEN:
		if node == 0:
			return False
		if node.row == S.row and node.col == S.col:
			return True
	return False
	

#Attach "P" as parent of "C" and calculate g,h and f
def AttachAndEval(C, P, BoardB):
	C.parent = P
	C.g = P.g + C.cost
	C.h = FindDistance(C.row, C.col, BoardB)
	C.f = C.h + C.g
	
	
#If "P" is the optimal parent, it is set as the parent for its kid and kid gets new g and f
def PropagatePathImprovements(P):
	for C in P.kids:
		if P.g + C.cost < C.g:
			C.parent = P
			C.g = P.g + C.cost
			C.f = C.g + C.h
			PropagatePathImprovements(C)
	
	
#Adds "S" to OPEN based on S.f
def AddToOPEN(S, OPEN, Board):
	OPEN.append(S)
	if Board[S.row][S.col] != 'A' and Board[S.row][S.col] != 'B':
		Board[S.row][S.col] = '*'

	 
#Reads the input file to matrix "Board", finds coordinates for "A" and "B", number of rows
#	and columns, sets up OPEN and CLOSED list, creates first node in "A", contains the
#	agenda loop.
#	Based on the A* supplement.
#	Assume there's allways just one "A" and "B". "A" and "B" are given coordinates
#	[row,column]
def main():
	Board = []
	BoardLine = []
	BoardA = []
	BoardB = []
	Created = []
	CreatedLine = []
	CreatedLetter = None
	Rowi = 0
	Coli = 0
#Find A and B, load the board into "Board", make a matrix "Created"
	for line in stdin:
		BoardLine = []
		CreatedLine = []
		Coli = 0
		for letter in line:
			if letter == 'A':
				BoardA.append(Rowi)
				BoardA.append(Coli)
			elif letter == 'B':
				BoardB.append(Rowi)
				BoardB.append(Coli)
			BoardLine.append(letter)
			CreatedLine.append(CreatedLetter)
			Coli += 1
		Board.append(BoardLine)
		Created.append(CreatedLine)
		Rowi += 1
	MaxRow = len(Board)
	MaxCol = len(Board[0])
#Set up OPEN and CLOSED list, prepare the first node
	OPEN = []
	CLOSED = []
	CLOSED.insert(0,0)
	X = SearchNode(BoardA[0],BoardA[1], Board)
	X = InitiateNode(X, BoardB, None, Created, 0)
	AddToOPEN(X, OPEN, Board)
#Agenda Loop
	Solution = False
	SUCC = []
	while Solution == False:
		if len(OPEN) == 0:
			print("No solution")
			break
		X = OPEN.pop(0)
		CLOSED.insert(0, X)
		if Board[X.row][X.col] != 'A' and Board[X.row][X.col] != 'B':
			Board[X.row][X.col] = 'X'
		SUCC = GenerateSuccessors(X, MaxRow, MaxCol, BoardB, Board, Created)
		if Board[X.row][X.col] == 'B':
			Solution = True
			print("Solution!!")
			Board = UpdateBoard(X, Board)
		else:
			IsInCLOSED = None
			for S in SUCC:
				IsInCLOSED = InCLOSED(S, CLOSED)
				S = PreviouslyCreated(S, Created)
				X.kids.insert(0, S)
				if IsInCLOSED == False and InOPEN(S, OPEN) == False:
					AttachAndEval(S,X,BoardB)
					AddToOPEN(S, OPEN, Board)
				elif (X.g + X.cost) < S.g:
					AttachAndEval(S,X,BoardB)
					if IsInCLOSED:
						PropagatePathImprovements(S)
	Print(Board)

	
#Run the main()
if __name__ == "__main__":
    main()