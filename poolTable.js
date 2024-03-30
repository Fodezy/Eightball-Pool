// $(window).on("load", function (){

$(document).ready(function(){
    var cueBallFound = 0;
    var cueX = 0;
    var cueY = 0;
    var cuePos = {};

    const SVG_NS = "http://www.w3.org/2000/svg";
    var mPos = {};
    var objLine = {};
    var lineEl = null;
    


    
    // $('#poolTable').on('load', function() {
    //     var svgDoc = $('#poolTable')[0].contentDocument;
    //     var svgRoot = svgDoc.documentElement;
    $.ajax({
        url: '/table-1.svg',
        type: 'GET',
        dataType: 'html',
        success: function(response)
        {
            $('#poolTable').html(response);
            // var svg = document.querySelector('#lines');

            $('#poolTable').find('circle').on('mouseover', function(e)
            {
                var id = $(this).attr('id');
                var cx = $(this).attr('cx');
                var cy = $(this).attr('cy');

                if(id == 0)
                {
                    $('#poolTable').addClass('inactive');
                    $('#lines').addClass('active');
                    // alert("HIT")
                    // alert('Ball ID: ' + id + '\nPosition: (' + cx + ', ' + cy + ')');
                    cueFound = 1;

                    var bbox = this.getBBox();
                    // alert("Hit")   
                    var svgElement = $('#poolTable svg').get(0);
                    // alert("Hit")   


                    var point = svgElement.createSVGPoint();
                    // alert("Hit")
                    point.x = bbox.x + bbox.width / 2;
                    point.y = bbox.y + bbox.height  / 2;

                    // alert("X: " + point.x + "\ny: " + point.y);

                    var transformedPoint = point.matrixTransform(svgElement.getScreenCTM());
                    // alert("Hit")

                    cueX = transformedPoint.x - 408;
                    cueY = transformedPoint.y + 711;

                    // 350
                    // 

                    // cueX = 525;
                    // 355 + 460;
                    // cueY = 1370;
                    // 1185;

                    alert("X: " + cueX + "\ny: " + cueY);

                    $('#poolTable').css('zIndex', -1); // Use .css method to change z-index
                    // alert("Hit")
                    $('#lines').css('zIndex', 1);
                    // alert("Hit")


                    svg = document.querySelector("#lines");
                    // svg = 0;
                    setDrawing(svg)

                } else {
                    // alert('Ball ID: ' + id + '\nPosition: (' + cx + ', ' + cy + ')');
                }
            });
        }
    });
    



function setDrawing (svg) {

    function velocity(e) {
        let endPoint = objMousePosSVG(e);

        let vel = {}

        vel.x = -(endPoint.x - cueX) * 15;
        vel.y = -(endPoint.y - cueY) * 15;

        let velLen = Math.sqrt((vel.x * vel.x) + (vel.y * vel.y));

        if(velLen > 10000)
        {
            alert("LIM HIT")
            vel.x = (vel.x / 10000) * 100;
            vel.y = (vel.y / 10000) * 100;
        }

        return vel;
    }

    function objMousePosSVG(ev)
    {
        let pos = svg.createSVGPoint();
        pos.x = ev.clientX;
        pos.y = ev.clientY;
        let ctm = svg.getScreenCTM().inverse();
        pos = pos.matrixTransform(ctm);


        return pos;
    }

    svg.addEventListener("mousedown", (e) => 
    {
        mPos = objMousePosSVG(e);
        objLine.x1 = cueX;
        objLine.y1 = cueY;
        objLine.x2 = mPos.x;
        objLine.y2 = mPos.y;
        lineEl = drawLine(objLine, svg);
    });

    function drawLine(obj, parent) 
    {
        let line = document.createElementNS(SVG_NS, "line");
        for(let name in obj) 
        {
            if(obj.hasOwnProperty(name))
            {
                line.setAttributeNS(null, name, obj[name]);
            }
        }
        parent.appendChild(line);
        return line;
    }

    svg.addEventListener("mousemove", (e) => 
    {
        if(lineEl)
        {
            mPos = objMousePosSVG(e);
            objLine.x2 = mPos.x;
            objLine.y2 = mPos.y;
            updateLine(objLine, lineEl);
        }
    })

    function updateLine(obj, element) 
    {
        for(let name in obj)
        {
            if(obj.hasOwnProperty(name)) 
            {
                element.setAttributeNS(null, name, obj[name]);
            }
        }
        return element;
    }

    svg.addEventListener("mouseup", (e) => 
    {
        if(lineEl)
        {   
            // let distance = {};
            let distanceVel = {}
            alert("HIT")
            distanceVel = velocity(e);
            alert("HIT")
            distance = distanceVel;
            lineEl.remove();

            $.ajax({
                url: '/calcVel',
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify ({
                    velX: distanceVel.x,
                    velY: distanceVel.y
                }),
                success: function(data, status) {
                    alert("Data: " + data + "\nStatus: " + status);
                }
            });

            // document.getElementById('poolTable').style.zIndex = 1;
            document.getElementById('lines').style.zIndex = -1;

            // alert("Distance:\n x: " + distance.x + " |  y: " + distance.y);
            
            
            $.ajax({
                url: '/svgFiles',
                // cache: false,
                type: 'GET',
                dataType: 'html',
                success: function(response){

                    var splitString = response.split(":,:");

                    var index = 0;

                    // $('#poolTable').remove();

                    function displayPart() {
                        if(index < splitString.length)
                        {
                            $('#poolTable').html(splitString[index]);
                            index++;
                            setTimeout(displayPart, 10);
                        }
                    }

                    displayPart();
                },
                error: function(xhr, status, error) {
                    alert("Error:", status, error);
                    // Optionally, you can display an error message to the user
                    $('#content').html("<p>Error: Unable to load SVG file.</p>");
                }
            });

            lineEl.remove();
            $('#content').html('table-1.svg')


            lineEl = null;
            objLine = {};

            // call helper fucntion.
                // function should create all svg files based on the shot velocity
            
            // 
        }
    });

    svg.addEventListener("mouseout", (e) => 
    {
        if(lineEl)
        {   
            lineEl.remove();
            let distanceVel = {}
            distanceVel = velocity(e);
            distance = distanceVel;

            $.ajax({
                url: '/calcVel',
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify ({
                    velX: distanceVel.x,
                    velY: distanceVel.y
                }),
                sucsess: function(data, status) {
                    alert("Data: " + data + "\nStatus: " + status);
                }
            });

            document.getElementById('poolTable').style.zIndex = -1;
            document.getElementById('lines').style.zIndex = 
1;
            // alert("Distance:\n x: " + distance.x + " |  y: " + distance.y);
            

            // newSVG();
            lineEl = null;
            objLine = {};
        }
    });
}   
    // // code snippet credited to [https://stackoverflow.com/questions/53847463/i-am-drawing-line-using-svg-and-jquery-ui-i-want-to-draw-it-in-all-directions-bu]
    // // as I took heavy inspiration on how to create and draw a line from it
    



});

// });

    


