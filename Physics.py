import phylib;
import sqlite3
import os
import math 
import poolTable
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_RATE = 0.01;
# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """
        # this creates a generic phylib_object 
        # instance attributes
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;
        self.number = number
        self.pos = pos

    # add an svg method here
    # instance method
    def svg( self ):
        result = ""
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="%d" />\n""" % ( self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number], self.obj.still_ball.number);
        return result;

# create a rolling_ball class  
class RollingBall(phylib.phylib_object):
    # defines what arguments needed for this object type 
    def __init__(self, number, pos, vel, acc):
        #creates the instance atributes for this object type
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0);
        # creates a rolling_ball class for the object type 
        self.__class__ = RollingBall;
        self.number = number 
        self.pos = pos
        self.vel = vel
        self.acc = acc

    def svg( self ):
        result = ""
        result = """ <circle cx="%d" cy="%d" r="%d" fill="%s" id="%d" />\n""" % ( self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number], self.obj.rolling_ball.number );
        return result;
        

class Hole(phylib.phylib_object):
    def __init__(self, pos):
        phylib.phylib_object.__init__(self, 
                                      phylib.PHYLIB_HOLE,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0);
        self.__class__ = Hole;
        self.pos = pos

    def svg( self ):
        result = ""
        result = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % ( self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS );
        return result;

class HCushion(phylib.phylib_object):
    def __init__(self, y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, 0, None, None, None, 0.0, y)
        self.__class__ = HCushion  
        self.y = y

    def svg( self ):

        # used to adjust the borders of the cushions to the proper postions on the svg image
        if self.obj.hcushion.y == 0:
            y_pos = -25
        else: 
            y_pos = 2700

        self.y = y_pos

        return f"""<rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % y_pos



class VCushion(phylib.phylib_object):
    def __init__(self, x):
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      None, None, None,
                                      x, 0.0);
        self.__class__ = VCushion;
        self.x = x

    def svg( self ):
        
        if self.obj.vcushion.x == 0:
            x_pos = -25
        else:
            x_pos = 1350

        self.x = x_pos
        
        result = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % x_pos
        return result;
################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):  #modify this bit to change decinal placement 
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.8f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg( self ):
        result = "";
        # adds the header content to the result (header is was generated above as a constant)
        result += HEADER;

        # checks over each object within the table 
        for obj in self:
            # ignores null values to avoid seg faults
            if obj is not None:
                # grabs the svg methods for each object type and saves the html string within svg
                svg = obj.svg()
                # ignores any fualty or null values returned about 
                if svg is not None:
                    # adds the html strings to the result
                    result += svg

        # adds the footer to the reslut 
        result += FOOTER;

        # return the generated table segments as an html coded svg file
        return result;

    def roll(self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                # Create4 a new ball with the same number as the old ball
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                       Coordinate(0, 0),
                                       Coordinate(0, 0),
                                       Coordinate(0, 0))
                # Compute where it rolls to
                phylib.phylib_roll(new_ball, ball, t)
                # Add ball to table
                new += new_ball
            if isinstance(ball, StillBall):
                # Create a new ball with the same number and position as the old ball
                new_ball = StillBall(ball.obj.still_ball.number,
                                     Coordinate(ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y))
                # Add ball to table
                new += new_ball
        # Return the new table with updated ball positions
        return new

    def cueBall(self, table, xVel, yVel, shotID):
        db = Database() # create an instance of the DB
        xPos, yPos = 0, 0
        cueBall = None
        # total = 0

        # check the tabel for all objects until cue ball is found
        for ball in table:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                # print("hit 2")
                xPos = ball.obj.still_ball.pos.x
                yPos = ball.obj.still_ball.pos.y
                cueBall = ball

        # if cue ball was found calculate acceleration 
        if isinstance(cueBall, StillBall):
            cueBall.type = phylib.PHYLIB_ROLLING_BALL
            cueBall.obj.rolling_ball.number = 0
            cueBall.obj.rolling_ball.pos.x = xPos
            cueBall.obj.rolling_ball.pos.y = yPos

            cueBall.obj.rolling_ball.vel.x = xVel
            cueBall.obj.rolling_ball.vel.y = yVel


            speed = math.sqrt(xVel**2 + yVel**2)

            acc_x, acc_y = 0, 0

            if speed > VEL_EPSILON:
                drag = DRAG / speed
                acc_x = -(xVel) * drag
                acc_y = -(yVel) * drag
                cueBall.obj.rolling_ball.acc = Coordinate(acc_x, acc_y)

            # create a second table to be used to roll over 
            rollTable = table
            # total = 0
            # cond = 0

            pTable = poolTable.AnimateShot()
            frameCounter = 0

            # loop indefinitaly until the table is None
            fp = open('table-2.svg', 'w');
            while True:
                # print(table)
                startTime = table.time  # start time

                table = table.segment()  # segment the table
                if table is None:
                # think i need to add one more addition to the database
                    break

                # calculate the frameRate
                endTime = table.time
                timeSegment = endTime - startTime
                frameRate = timeSegment / FRAME_RATE
                frameRate = int(frameRate)
                # amt = 0
                # totalTableZero = 0

                
                # fp.write()
                # check if its the first table whcih hasnt segmented yet
                if math.isclose(rollTable.time, 0.0, abs_tol=1e-11):
                    # loop for 0 intil frameRate + 1
                    for frame in range(frameRate + 1):
                        # calculate the frame instance 
                        newFrame = frame * FRAME_RATE
                        # apply the role
                        newTable = rollTable.roll(newFrame)
                        # set the new time 
                        # write to db for the table, and table / ball ids
                        newTable.time = startTime + newFrame

                        # write directly to svg

                        pTable.getTable(newTable)
                        frameCounter = frameCounter + 1;


                        # tableID = db.writeTable(newTable)
                        # db.setTableShot(tableID, shotID)
                        # amt += 1

                    # totalTableZero += amt
                    # total += amt
                    # print("TABLE ONE amt: ", totalTableZero)
                # condition for every other table
                else:
                    # loop starts at one to avoid overlap with table 1
                    for frame in range(1, frameRate + 1):
                        newFrame = frame * FRAME_RATE
                        newTable = rollTable.roll(newFrame)
                        newTable.time = startTime + newFrame

                        pTable.getTable(newTable)
                        frameCounter = frameCounter + 1;
                        # write directly to svg

                        # tableID = db.writeTable(newTable)
                        # db.setTableShot(tableID, shotID)
                        

                # segment the rolling table 
                rollTable = rollTable.segment() 
            fp.close()
                        # amt += 1
                        # cond = 1
                    # print("ELSE TABLES amt: ", amt)
                    # total += amt
            # print("Total: ", total)

                # table 1 -> times 0 to 1.451  (add total frames: 145 + 1)  < -- includes table 0

                # table 2 -> time 1.4569 (add total frame: 1) not add

                # table 3 -> time 1.4573 (add total frame: 1) not add 

                # table 4 -> times 1.46 to 1.51 (add total frame: 5)

                # table 5 -> times 1.52 to 2.03 (add total frame: 52)

                # table 6 -> times 2.04 to 2.45 (add total frame: 41)

                # table 7 -> times 2.46 to 2.65 (add total frame: 20)

                # table 8 -> times 2.66 to 3.75 (add total frame: 110)

                # table 9 -> times 3.76 to 3.82 (add total frame: 6)

                # table 10 -> times 3.83 to 5.95 (add total frame: 213)

                # total frames to add: 594  <-- includes table with time 0.00

                # amt = 0

                # this if statement and code inside should be right
                # if math.isclose(tempTable.time, 0.0, abs_tol=1e-11): # <-- checks if table is starting table
                #                                                     # as we need a non segmented table to get the first frames before contact is made
                #     # print(tempTable)
                #     tableID = db.writeTable(tempTable)
                #     print("Starting table: ", frameRate)

                #     for frame in range(1, frameRate):
                #         total += 1
                #         amt += 1

                        # newFrame = frame * FRAME_RATE
                        # newTable = tempTable.roll(newFrame)
                        # newTable.time = startTime + newFrame
                        # tableID = db.writeTable(newTable)
                        # db.setTableShot(tableID, shotID)
                        

                #     # db.writeTable(table)
                #     total += 1
                #     # print(amt) 

                # elif frameRate == 0: # wrong
                # #     # print(table)
                # #     print("1 Frame Tables: ",frameRate)
                #     for frame in range(frameRate + 1):
                #         total += 1

                #         newFrame = frame * FRAME_RATE
                #         newTable = table.roll(newFrame)
                #         newTable.time = startTime + newFrame
                #         tableID = db.writeTable(newTable)
                #         tableID = db.setTableShot(tableID, shotID)

                # else: # wrong


                #     # print(table)
                #     print("Normal tables: ", frameRate)
                #     for frame in range(1, frameRate + 1):
                #         total += 1

                #         newFrame = frame * FRAME_RATE
                #         newTable = table.roll(newFrame)
                #         newTable.time = startTime + newFrame
                #         tableID = db.writeTable(newTable)
                #         db.setTableShot(tableID, shotID)
                # # db.writeTable(table)
                # tempTable = tempTable.segment()
                # print(total)


class Database():
    """
    DataBase class, used to:
        - Initialize the connection and reset the db file if specified 
        - Create teh database and tables  
        - Read from the database 
        - Write to the database 
        - Commit and Close on the connections
    """
    def __init__(self, reset=False):
        # reset = True
        # check if file exits if so remove
        if reset is True:
            if os.path.exists("phylib.db"):
                os.remove("phylib.db")
        
        # create and connect to db
        self.connect = sqlite3.connect("phylib.db")
        self.cursor = self.connect.cursor()


    # create all tables 
    def createDB( self ):
        createBall = """ 
        CREATE TABLE IF NOT EXISTS Ball (
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
            BALLNO INTEGER NOT NULL, 
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
        );
        """

        createTTable = """
        CREATE TABLE IF NOT EXISTS TTable (
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
            TIME FLOAT NOT NULL
        );
        """

        createBallTable = """
        CREATE TABLE IF NOT EXISTS BallTable (
            BALLID INTEGER NOT NULL, 
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY(BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID)
        );
        """

        createShot = """
        CREATE TABLE IF NOT EXISTS Shot (
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL, 
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY(PLAYERID) REFERENCES Player(PLAYERID),
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
        );
        """

        createTableShot = """
        CREATE TABLE IF NOT EXISTS TableShot (
            TABLEID INTEGER NOT NULL,
            SHOTID INTEGER NOT NULL,
            FOREIGN KEY(TABLEID) REFERENCES TTable(TABLEID),
            FOREIGN KEY(SHOTID) REFERENCES Shot(SHOTID)
        );
        """

        createGame = """
        CREATE TABLE IF NOT EXISTS Game (
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT,
            GAMENAME VARCHAR(64) NOT NULL
        );
        """

        createPlayer = """
        CREATE TABLE IF NOT EXISTS Player (
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY(GAMEID) REFERENCES Game(GAMEID)
        );
        """

        self.cursor.execute(createBall)
        self.cursor.execute(createTTable)
        self.cursor.execute(createBallTable)
        self.cursor.execute(createShot)
        self.cursor.execute(createTableShot)
        self.cursor.execute(createGame)
        self.cursor.execute(createPlayer)
        self.connect.commit()
        self.connect.close()

    def readTable( self, tableID):
        """
            - Retrieves the balls values 
            - Retrieves the time 
            - Adds the ball type to table
                - if rolling ball calculate acceleration
            - set the time 
            - return the table
        """
        self.__init__()
        table = Table()

        newTableID = tableID + 1
        # print(f"{newTableID} : {tableID}")

        self.cursor.execute("SELECT * FROM TTable WHERE TABLEID = ?", (newTableID,))
        tables = self.cursor.fetchall()

        if len(tables) == 0:
            # print("WAS NONE")
            return None

        self.cursor.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL FROM Ball
                            INNER JOIN BallTable
                            ON Ball.BALLID = BallTable.BALLID
                            WHERE BallTable.TABLEID = ? """, (newTableID,))
        ballValues = self.cursor.fetchall()

        self.cursor.execute("SELECT TIME FROM TTable WHERE TABLEID = ?", (newTableID,))
        time = self.cursor.fetchone()
        # print(time[tableID])
        # print(ballValues)

        for types in ballValues:
            ballID, ballNO, xPos, yPos, xVel, yVel = types
            if (xVel is None or xVel == 0) and (yVel is None or yVel == 0):
                # print("Still ball")
                sb = StillBall(ballNO, Coordinate(xPos, yPos))
                table += sb
            else:
                # print("Rolling ball");
                # speed_a = math.sqrt(float(xVel) * float(xVel) 
                #                 + float(yVel) * float(yVel))
                acc_x = 0
                acc_y = 0
                speed = math.sqrt(xVel**2 + yVel**2)
                if speed > VEL_EPSILON:
                    drag = DRAG / speed
                    acc_x = -(xVel) * drag
                    acc_y = -(yVel) * drag
                    acc_epsilon_update_a = Coordinate(acc_x, acc_y)

                rb = RollingBall(ballNO, Coordinate(xPos, yPos), Coordinate(xVel, yVel), acc_epsilon_update_a)
                table += rb
    
        table.time = time[0]
        # print(table)
        self.close()
        return table

    def writeTable( self, table):
        """
            - Inserts the Time into the TTable
            - Inserts ball values int the Ball depending on ball type 
            - Insert ball and table ids into BallTable
            - Return tableID 
        """
        # print(table)
        self.__init__()

        time = table.time

        self.cursor.execute("INSERT INTO TTable (TIME) VALUES (?)", (time,))
        self.cursor.execute("SELECT TABLEID FROM TTable")
        tableID = self.cursor.lastrowid - 1;
        # print(tableID)

        for i,objt in enumerate(table):
            if (objt is not None) and (isinstance(objt, StillBall) or isinstance(objt, RollingBall)):
                if isinstance(objt, StillBall):
                    self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS) VALUES (?, ?, ?)", (objt.obj.still_ball.number, objt.obj.still_ball.pos.x, objt.obj.still_ball.pos.y,))
                # print(dir(objt.obj.still_ball.number))
                # print(objt.obj.still_ball.number)
                # print("WAS Stll Ball")
                elif isinstance(objt, RollingBall):
                    self.cursor.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?)", (objt.obj.rolling_ball.number, objt.obj.rolling_ball.pos.x, objt.obj.rolling_ball.pos.y, objt.obj.rolling_ball.vel.x, objt.obj.rolling_ball.vel.y))
                # print("WAS Rolling Ball")

                ballID = self.cursor.lastrowid

                self.cursor.execute("INSERT INTO BallTable (TABLEID, BALLID) VALUES (?, ?)", (tableID + 1, ballID))

        self.close()
        return tableID

    def getGame( self, gameID ):
        """
            - Selects the Game, Player One, & Player Two's names from the table
              on certian conditions
            - Return gameValue
        """
        self.__init__()

        self.cursor.execute(f"""SELECT 
                                (SELECT Game.GAMENAME FROM Game WHERE Game.GAMEID = ?),
                                (SELECT Player.PLAYERNAME FROM Player WHERE Player.GAMEID = ? ORDER BY Player.PLAYERID ASC LIMIT 1), 
                                (SELECT Player.PLAYERNAME FROM Player WHERE Player.GAMEID = ? ORDER BY Player.PLAYERID DESC LIMIT 1)
                            FROM PLAYER 
                            INNER JOIN Game
                            ON Player.GAMEID = Game.GAMEID
                            WHERE Player.GAMEID = ?  
                            LIMIT 1
                            """, (gameID, gameID, gameID, gameID))
        
        gameValues = self.cursor.fetchone()
        # print(gameValues)
        self.close()
        return gameValues

    def setGame( self, gameName, p1Name, p2Name):
        """
            - Insert Game, Player One, & Player Two's names into the db
            - Return the gameID
        """
        self.__init__()

        self.cursor.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))

        self.cursor.execute("""SELECT GAMEID FROM Game 
                            WHERE GAMENAME = ?""", (gameName,))
        
        gameID = self.cursor.fetchone()[0]

        self.cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (p1Name, gameID))
        self.cursor.execute("INSERT INTO Player (PLAYERNAME, GAMEID) VALUES (?, ?)", (p2Name, gameID))

        self.close()
        return gameID

    def newShot( self, gameName, playerName ):
        """
            - Retrieve the Game & Player ID's from db on certian condtions
            - Unpack the results returned and Insert them into the db
            - Retrieve the ShotID and Return that 
        """
        self.__init__()
        
        self.cursor.execute("""SELECT Game.GAMEID, Player.PLAYERID FROM Game 
                            INNER JOIN Player
                            ON Game.GAMEID = Player.GAMEID
                            WHERE Game.GAMENAME = ? AND Player.PLAYERNAME = ?""", (gameName, playerName))
        result = self.cursor.fetchone()

        if result:
            gameID, playerID = result

         
        self.cursor.execute(""" INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)""", (playerID, gameID))

        self.cursor.execute("""SELECT SHOTID FROM Shot
                            WHERE GAMEID = ? AND PLAYERID = ?""", (gameID, playerID))
        
        shotID = self.cursor.fetchone()[0]
        # print(shotID)

        self.close()
        
        return shotID

    def setTableShot(self, tableID, shotID):
        """
            - Insert Table & Shot ID's into the db 
        """
        self.__init__()

        self.cursor.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (tableID, shotID))

        self.close()



    def close( self):
        """
        Commits  the connection and closes on the connection
        """
        self.connect.commit()
        self.cursor.close() 


class Game():
    """
    Initializes the Game logic (table values) and the Players information 
        - Creates constructor one for the GameID and retrieves the data from getGame 
        - Creates constructor two for the rest of the values and retrieves the gameID from setGame
            - these are added as attributes to the Game class 
        - Throws a Type Error if invalid arguments are passed 
    """
    
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        self.db = Database()
        if (gameID is not None) and (gameName is None) and (player1Name is None) and  (player2Name is None):
            # print("HIT 1")
            self.gameID = gameID + 1
            self.gameName, self.player1Name, self.player2Name = self.db.getGame(gameID)
            # print(self.gameName, self.player1Name, self.player2Name)

        elif (gameID is None) and (gameName is not None) and (player1Name is not None) and  (player2Name is not None):
            # print("HIT 2")
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            # print(gameID)

        else:
            raise Exception(TypeError)

    def shoot( self, gameName, playerName, table, xvel, yvel):
        """
        Creates the logic for taking a turn and hitting the cue ball
        Then simulates the rest of the turn frame by frame
        """
        self.db = Database()
        
        # shotID = self.db.newShot(gameName, playerName)

        table.cueBall(table, xvel, yvel, 1)