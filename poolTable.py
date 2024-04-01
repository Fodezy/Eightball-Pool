import Physics
import phylib

import os


class Initialize_Table():
    """
    Initializes the table with the pool balls in the starting positions
    """

    def __init__(self, table):
        self.table = table

    def setCueBall(self):
        """
        Sets the position of the cueBall
        """

        pos = Physics.Coordinate(675, 2025)
        sb = Physics.StillBall(0, pos) # sets the cue ball
        self.table += sb



    def setRack(self, x, y, num):
        """
        Sets the rack of 
        """
        pos = Physics.Coordinate(x, y)
        sb = Physics.StillBall(num, pos)
        self.table += sb


class SetTablePos():

    def createTable(self):
        table = Physics.Table() 
        initTable = Initialize_Table(table)  # offset: x = +-(28.5 or 57) y = -50
                                # with nudge x = +- (31 or 62) y = -53

        initTable.setCueBall()

        # need a slight nudge between each ball
        # row one
        initTable.setRack(675, 675, 1) #ball one

        # row two
        initTable.setRack(644, 622, 2) #ball one
        initTable.setRack(705, 622, 3) #ball one

        # row three
        initTable.setRack(675, 569, 8) #ball one
        initTable.setRack(613, 569, 4) #ball one
        initTable.setRack(736, 569, 5) #ball one

        # row four
        initTable.setRack(582, 516, 6) #ball one
        initTable.setRack(644, 516, 7) #ball one
        initTable.setRack(705, 516, 9) #ball one
        initTable.setRack(767, 516, 10) #ball one

        # row five
        initTable.setRack(551, 463, 11) #ball one
        initTable.setRack(613, 463, 12) #ball one
        initTable.setRack(675, 463, 13) #ball one
        initTable.setRack(737, 463, 14) #ball one
        initTable.setRack(795, 463, 15) #ball one

        # print(table)

        svg = table.svg()
        with open(f"table-1.svg", "w") as file:
            file.write(svg);

        return table


class AnimateShot():

    def __init__(self):
        self.db = Physics.Database(reset = True)
        self.cueBallString = 0

    def initDB(self, table):
        self.db.createDB()
        self.db.writeTable(table)

        game = Physics.Game(gameName="Game 1", player1Name="Eric", player2Name="Peter")
        return game

    def getTable(self, table):
    
        svgContent = table.svg()

        svgContent = ":,:" + svgContent 

        # print(svgContent)

        with open("table-2.svg", "a") as fp:
            fp.write(svgContent)

    def writeCueBall(self, svgString, table):
        newBallIDS = []
        isCueBall = True
        newSVG = svgString

        for obj in table:
            if obj is not None:
                if isinstance(obj, Physics.RollingBall):
                    newBallIDS.append(obj.obj.still_ball.number)

                elif isinstance(obj, Physics.StillBall):
                    newBallIDS.append(obj.obj.rolling_ball.number)

        if 0 not in newBallIDS:
            print("hit: ", obj)  
            pos = Physics.Coordinate(675, 2025)
            sb = Physics.StillBall(0, pos) # sets the cue ball
            table += sb
            newSVG = table.svg()

        return table, newSVG


class GameLogic():

    def __init__(self):
        self.ballID = []
        self.newBallIDS = []
        self.beforeBallCount = 0
        self.afterBallCount = 0

        self.playerOne = 0 
        self.playerOneRange = -1
        self.playerOneBallCount = 7

        self.playerTwo = 1
        self.playerTwoRange = -1
        self.playerTwoBallCount = 7

        self.currentPlayerID = 0

        self.gameWinner = 0

    def setCurrentPlayer(self, playerID):
        self.currentPlayerID = playerID

    def switchPlayer(self):

        if self.currentPlayerID == 0:
            self.currentPlayerID = 1
        elif self.currentPlayerID == 1:
            self.currentPlayerID = 0
        

    def shotStatus(self, table):
        ballID = []

        for obj in table:
            if obj is not None:
                if isinstance(obj, Physics.RollingBall):
                    self.ballID.append(obj.obj.still_ball.number)

                elif isinstance(obj, Physics.StillBall):
                    self.ballID.append(obj.obj.rolling_ball.number)

    def afterSatus(self, table):
        isCueBallSunk = False
        isEghtBallSunk = False

        for obj in table:
            if obj is not None:
                if isinstance(obj, Physics.RollingBall):
                    self.newBallIDS.append(obj.obj.still_ball.number)

                elif isinstance(obj, Physics.StillBall):
                    self.newBallIDS.append(obj.obj.rolling_ball.number)

        beforeLen = len(self.ballID)
        afteridlen = len(self.newBallIDS)

        diffrence = beforeLen - afteridlen

        playerBallCount = self.ballRangeCount(self.currentPlayerID)


        if diffrence > 0:

            if self.playerOneRange == -1:
                ballNum = self.firstBallSunk()
                self.setBallRange(ballNum)

            # add helper function
            isCueBallSunk = self.isCueBallSunk(beforeLen, afteridlen)
            isEigthBallSunk = self.isEigthBallSunk(afteridlen)
            
            if isEigthBallSunk and playerOneBallCount == 0: # and more then just 8 ball left for player
                return 1 #player one winner

            elif isEigthBallSunk and playerTwoBallCount == 0:
                return 2 #player two winner

            elif isEigthBallSunk:
                # end game and determine winner by switching player id
                self.switchPlayer()
                return 8

            # if cueball sunk and playerball sunk
            if self.currentPlayerID == self.playerOne:
                if (self.playerOneBallCount - playerBallCount) > 0 and isCueBallSunk:
                    hit = 1
                    # reset cueBall

            elif self.currentPlayerID == self.playerTwo:
                if (self.playerTwoBallCount - playerBallCount) > 0 and isCueBallSunk:
                    hit = 1
                    # reset cueBall
              
            elif isCueBallSunk:
                self.switchPlayer()
                # reset cueBall
            

            if self.currentPlayerID == self.playerOne:
                if (self.playerOneBallCount - playerBallCount) == 0:
                    self.switchPlayer()

            elif self.currentPlayerID == self.playerTwo:
                if (self.playerTwoBallCount - playerBallCount) == 0:
                    self.switchPlayer()


            

        else:
            # switch player turn 
            self.switchPlayer()

        
        print("P1BBCount: ", self.playerOneBallCount, "ID: ", self.playerOneRange)
        print("P2BBCount: ", self.playerTwoBallCount, "ID: ", self.playerTwoRange)

        self.playerOneBallCount = self.ballRangeCount(self.playerOneRange)
        self.playerTwoBallCount = self.ballRangeCount(self.playerTwoRange)

        print("P1ABCount: ", self.playerOneBallCount)
        print("P2ABCount: ", self.playerTwoBallCount)

        self.ballID.clear()
        self.newBallIDS.clear()

        
        return 0

    # def gameWinner(self, playerID):
        # if 


    # temp code, need to do this check in the cueBall method in Physics
    def firstBallSunk(self):
        firstId = 0
        missing = [id for id in self.ballID if id not in self.newBallIDS];

        for i in range(len(missing)):
            if missing[i] != 0 or missing[i] != 8:
                print(missing)
                if missing is not None:
                    firstId = missing[0]

        return firstId

    def setBallRange(self, ballNum):

        if ballNum > 0 and ballNum < 8:
            if self.currentPlayerID == 0:
                self.setRange(0, 0)
                self.setRange(1, 1)
            elif self.currentPlayerID == 1:
                self.setRange(1, 0)
                self.setRange(0, 1)
        
        if ballNum > 8 and ballNum < 16:
            if self.currentPlayerID == 0:
                self.setRange(0, 1)
                self.setRange(1, 0)
            elif self.currentPlayerID == 1:
                self.setRange(1, 1)
                self.setRange(0, 0)

    def setRange(self, playerID, playerRange):
        if playerID == 0:
            self.playerOneRange = playerRange
        elif playerID == 1:
            self.playerTwoRange = playerRange

    def isCueBallSunk(self, beforeLen, afterLen):

        # print(self.newBallIDS)

        for j in range(0, afterLen):
            if self.newBallIDS[j] == 0:
                print("CueBall found: ", self.newBallIDS[j])
                return False
            else:
                print("CueBall not found: ")
        
        return True

    def isEigthBallSunk(self, afterLen):

        for i in range(0, afterLen):
            if self.newBallIDS[i] == 8:
                print("8 ball found: ", self.newBallIDS[i])
                return False
            else:
                print("8 ball not found: ")
        
        return True


    # def addCueBall():


    def ballRangeCount(self, playerRange):

        counter = 0
        for i in range(len(self.newBallIDS)):
            if playerRange == 0:
                if self.newBallIDS[i] > 0 and self.newBallIDS[i] <= 7:
                    counter += 1
            elif playerRange == 1:
                if self.newBallIDS[i] > 8 and self.newBallIDS[i] <= 15:
                    counter += 1

        return counter








