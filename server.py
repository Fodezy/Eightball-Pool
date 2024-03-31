import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

import re
import os

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

from Physics import *
import math
import poolTable

import json





# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    # def __init__(self):
        # self.table = pTable.createTable()

    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        # print(parsed)


        # splits the path at the dash to retrive the table part of the path
        begining = re.split('-', parsed.path)
        begining[0] += "-"  # adds the dash back as its needed 
        begining[0] = begining[0].replace('/', '') # removes the slash as it is not needed since its not within the path name 
        if begining[0] == 'table-':  # checks if path was a table file, if its not it would cause an out of bounds error since it would not have split
            num_end = re.split('\.', begining[1])  #seperates the number and the .svg from the path by looking for "."
            num_end[1] = '.' + num_end[1]  # adds the period back as its need for the file path 
            end = num_end[1] # saves the number in its own variable
    
        
        # check if the web-pages matches the list for the form shoot.html
        if parsed.path in [ '/shoot.html' ]:

            # retreive the HTML file and open the file
            fp = open( '.'+self.path );
            # read the content
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
            

        # check if the web-pages matches the list and naming structure for a table file
        elif begining[0] == 'table-' and end == '.svg':
            # creates the file path by concatanating the strings together 
            file_path = begining[0] + num_end[0] + end
            
            # print(file_path)

            # checks if the file path is valid or not
            if os.path.isfile(file_path):
                    # open the svg file
                    fp = open(file_path)
                    content = fp.read();

                    self.send_response(200)
                    #type is scg and html since that the file type
                    self.send_header('Content-type', 'image/svg+xml')
                    self.send_header("Content-length", len( content ))
                    self.end_headers()

                    self.wfile.write( bytes(content, "utf-8") )
                    fp.close()
                    

        # If the file does not exist or the path does not match, return 404
            else: self.send_error(404, "File Not Found: %s" % self.path)

        elif parsed.path in [ '/poolTable.html' ]:

            fp = open('.' + self.path)
            content = fp.read()

            self.send_response(200)
            # self.send_header("Content-type", "image/svg+xml") #text/html
            self.send_header("Content-type", "text/html") #text/html
            self.send_header("Content-length", len( content ))
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )
            fp.close()

        elif parsed.path in ['table-1.svg']:
            with open('table-1.svg', 'r') as fp:
                content = fp.read()

            self.send_response(200)
            # self.send_header("Content-type", "image/svg+xml") #text/html
            self.send_header("Content-type", "text/html") #text/html
            self.send_header("Content-length", len( content ))
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )
            fp.close()

        elif parsed.path in ['/svgFiles']:

            with open('table-2.svg', 'r') as fp:
                content = fp.read()
                # contentSplit = content.split(':,:')

            # for content in contentSplit:
                # print(content)
            

            self.send_response(200)
            # self.send_header("Content-type", "image/svg+xml") #text/html
            self.send_header("Content-type", "text/html") #text/html
            self.send_header("Content-length", len( content ))
            self.end_headers()

            self.wfile.write( bytes(content, "utf-8") )
            fp.close()


        
        elif parsed.path.endswith(".js"):
            # Assuming your JS files are stored in the same directory as your Python script
            try:
                with open('.' + parsed.path, 'r') as file:
                    content = file.read()
                    self.send_response(200)
                    self.send_header("Content-type", "application/javascript")
                    self.send_header("Content-length", len(content))
                    self.end_headers()
                    self.wfile.write(bytes(content, "utf-8"))
                    
            except FileNotFoundError:
                self.send_error(404, "File Not Found: %s" % parsed.path)       
        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):
        global table
        global anShot
        global game
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );

        
        # checks for if this path is requested which it is if the shoot button is submited 
        if parsed.path in [ '/display.html' ]:

            # 1. Recive form data from html page form
            form = cgi.FieldStorage ( fp = self.rfile,
                                     headers = self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                'CONTENT_TYPE':
                                                    self.headers['Content-Type']
                                                }
                                    )
            # print("ENTERED POST REQUEST\n")
            # print(parsed.path)

            # 2. used to check the files within working directory 
            for fname in os.listdir('.'):
            # same file name structure checking for table as used above
                begining = re.split('-', fname)
                begining[0] += "-"
                begining[0] = begining[0].replace('/', '') 
                if begining[0] == 'table-':
                    num_end = re.split('\.', begining[1])
                    num_end[1] = '.' + num_end[1]
                    end = num_end[1]
                    file_path = begining[0] + num_end[0] + end

                    # used to remove any table-d.svg files in the directory
                    os.remove(file_path)
                    # print("Removing file: ", file_path)

            #  this is how to access the form data from shoot.html
            # sb_number = form.getvalue('sb_number')
            # print(sb_number)


            # 3. computes the acceleration of the rolling ball using form data 
            speed_a = math.sqrt(float(form.getvalue('rb_dx')) * float(form.getvalue('rb_dx')) 
                                + float(form.getvalue('rb_dy')) * float(form.getvalue('rb_dy')))

            acc_epsilon_update_a = Coordinate(0, 0)
            acc_epsilon_update_a.x = -float(form.getvalue('rb_dx')) / speed_a * DRAG
            acc_epsilon_update_a.y = -float(form.getvalue('rb_dy')) / speed_a * DRAG

            # print("Speed_a: ", speed_a)
            # print("Acc_eps.x: ", acc_epsilon_update_a.x)
            # print("Acc_eps.y: ", acc_epsilon_update_a.y)


            # 4. create a table and input data based on the fields from the form 
            table = Table();
            pos = Coordinate(0, 0);
            vel = Coordinate(0, 0);
            acc = Coordinate(0, 0);
            ball_num = 0

            pos.x = float(form.getvalue('sb_x'))
            pos.y = float(form.getvalue('sb_y'))
            ball_num = int(form.getvalue('sb_number'))
            sb = StillBall(ball_num, pos)

            pos.x = float(form.getvalue('rb_x'))
            pos.y = float(form.getvalue('rb_y'))
            vel.x = float(form.getvalue('rb_dx'))
            vel.y = float(form.getvalue('rb_dy'))
            acc.x = acc_epsilon_update_a.x
            acc.y = acc_epsilon_update_a.y
            ball_num = int(form.getvalue('rb_number'))
            rb = RollingBall(ball_num, pos, vel, acc)

            table += sb
            table += rb

            # used to see table output and timing, made to visualize the data
            # print(table);

            # while True:
            #     table = table.segment();
            #     if table is None:
            #         break
            #     print(table)

            # 5. saves the tables made into the working directory 
            file_index = 0
            # creates infinte loop until broken
            while True:
                # saves the table images into the svg variable
                svg = table.svg();
                # creates a new svg file based on the table naming structer
                fp = open(f"table-{file_index}.svg", "w")
                # writes into the file
                fp.write(svg);
                # close the file
                fp.close()
                # increase the index
                file_index += 1;

                # add the new table segemnt to the table
                table = table.segment();
                # repeate process until table is null, when it is break from while loop
                if table is None:
                    break;
            
            # retireve and store field values 
            sb_num = form.getvalue('sb_number')
            sb_x = form.getvalue('sb_x')
            sb_y = form.getvalue('sb_y')

            rb_num = form.getvalue('rb_number')
            rb_x = form.getvalue('rb_x')
            rb_y = form.getvalue('rb_y')
            rb_dx = form.getvalue('rb_dx')
            rb_dy = form.getvalue('rb_dy')


            # used to retrieve all table-%d.svg files within the working direcotry and save them within an array 
            file_path = []
            for fname in os.listdir('.'):
                begining = re.split('-', fname)
                begining[0] += "-"
                begining[0] = begining[0].replace('/', '') 
                if begining[0] == 'table-':
                    num_end = re.split('\.', begining[1])
                    num_end[1] = '.' + num_end[1]
                    end = num_end[1]
                    fname = begining[0] + num_end[0] + end

                    file_path.append(fname)

            # sort the vaoues within the array from smallest to largest so they can be displayed in order
            file_path.sort(key=lambda fname: int(fname.split('-')[1].split('.')[0]))


            # used to create the img tag and display the table svg files 
            svg_images = ""
            counter = 0
            for fname in file_path:
                svg_images += f'\
                <h3> Image: {counter}</h3>\
                <img src ="{fname}" alt="svg pool segment display" \n>'
                counter += 1
                    
            # an html string i generated to nicely display the og values from sb and rb in their own tables and layred the imgs ontop of each other 
            # back button is below all images to go back to the shoot.html form 
            content = f"""
            <html>
<head>
    <title>Table Results</title>
    <style>
        .table-container {{
            float: left;
            margin-right: 20px;
        }}
        .clear {{
            clear: both;
        }}
        .image-container img {{
            display: block; 
            margin-bottom: 20px; 
        }}
    </style>
</head>
<body>
    <div class="table-container">
        <h3>Still Ball Values:</h3>
        <table border="1"> 
            <tr>
                <th>Ball Number</th>
                <th>X Position</th>
                <th>Y Position</th>
            </tr>
            <tr>
                <td>{sb_num}</td>
                <td>{sb_x}</td>
                <td>{sb_y}</td>
            </tr>
        </table>
    </div>
    <div class="table-container">
        <h3>Rolling Ball Values:</h3>
        <table border="1"> 
            <tr>
                <th>Ball Number</th>
                <th>X Position</th>
                <th>Y Position</th>
                <th>X Velocity</th>
                <th>Y Velocity</th>
                <th>X Acceleration</th>
                <th>Y Acceleration</th>
            </tr>
            <tr>
                <td>{rb_num}</td>
                <td>{rb_x}</td>
                <td>{rb_y}</td>
                <td>{rb_dx}</td>
                <td>{rb_dy}</td>
                <td>{str(acc_epsilon_update_a.x)}</td>
                <td>{str(acc_epsilon_update_a.y)}</td>
            </tr>
        </table>
    </div>
    <div class="clear"></div>
    <h3> Pool segment Images </h3>
    <div>
        <body class = "image-container">
            {svg_images}
        </body>
    </div>
    <a href='shoot.html'>
        <button>Back</button>
    </a>
</body>
</html>"""



            # used to send the html formated string the the server 
                
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()

            # Send HTML content to the browser
            self.wfile.write(bytes(content, "utf-8"))
            # get data send as Multipart FormData (MIME format)

        elif parsed.path in [ '/calcVel']:

            try:
                postData = self.rfile.read(int(self.headers['Content-Length']))
                velData = json.loads(postData.decode("utf-8"))
                velx = velData['velX']
                vely = velData['velY']

                print(velx, " | ", vely)


                # anShot.getTable(table)
                # print(table)
                table = game.shoot("Game 1", "Eric", table, velx, vely)
                print(table)

                # r = Retreive()
                # vel = r.calculateVel(velx, vely)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({'result': 'success'})
                self.wfile.write(response.encode('utf-8'))

                # game.shoot("Game 1", "Eric", table, velx, vely)


            except json.JSONDecodeError as e:
                self.send_error(400, 'Invalid JSON data')
                print(e.msg)

        elif parsed.path in ['/writeStarter']:
            try: 
                content_length = int(self.headers['Content-Length'])
                svg = self.rfile.read(content_length).decode('utf-8')

                # print(svg)

                with open(f"table-1.svg", "w") as file:
                    file.write(svg);

                fp = open("table-2.svg", "w")
                fp.write("")
                fp.close()

                self.send_response(200)
                self.send_header('Content-type', 'html')
                self.end_headers()
                self.wfile.write(b'SVG script received successfully')
            except:
                self.send_error(400, 'Invalid JSON data')
                print(e.msg)

        
            
        else:
            # generate 404 for POST requests that aren't the file above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

if __name__ == "__main__":

    # print(table)

    anShot = poolTable.AnimateShot()
    pTable = poolTable.SetTablePos()

    table = pTable.createTable()
    game = anShot.initDB(table)
    # anShot.getTable()

    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    # used as a hyper link to quckly access the web application 
    print(f'http://localhost:{int(sys.argv[1])}')
    print(f'http://localhost:{int(sys.argv[1])}/shoot.html')
    print(f'http://localhost:{int(sys.argv[1])}/poolTable.html')
    httpd.serve_forever();
