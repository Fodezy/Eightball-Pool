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

    def initDB(self, table):
        self.db.createDB()
        self.db.writeTable(table)

        game = Physics.Game(gameName="Game 1", player1Name="Eric", player2Name="Peter")
        return game

    # def write_svg(table_id, table):
    #     directory = "svgFiles"
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)

    #     # Use an integer for the filename (zero-padded)
    #     filename = f"{directory}/table{table_id:05d}.svg"
    #     with open(filename, "w") as fp:
    #         fp.write(table.svg())

    def getTable(self, table):
    
        svgContent = table.svg()

        svgContent = ":,:" + svgContent 

        # print(svgContent)

        with open("table-2.svg", "a") as fp:
            fp.write(svgContent)






