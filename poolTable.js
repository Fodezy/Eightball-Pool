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

    var gameOver = 0
    

    $.ajax({
        url: '/table-1.svg',
        type: 'GET',
        dataType: 'html',
        success: function(response)
        {
            $('#poolTable').html(response);
            // var svg = document.querySelector('#lines');
        }
    });

$('#poolTable').on('mouseover', 'circle', function(e){

    // alert("HIT")
    var id = $(this).attr('id');
    newShot(id, e)
})




function newShot(id, e) 
{
        if(id == 0)
        {
            cueFound = 1;
            var svgElement = $('#poolTable svg').get(0); // Get the SVG element

            $('#poolTable').css('zIndex', -1); // Use .css method to change z-index
            $('#lines').css('zIndex', 1);
            // alert("Hit")
            svg = document.querySelector("#lines");

            setDrawing(svg);
        } else if (gameOver == 8) 
        {
            alert("GAME OVER")
        }
        else if (gameOver == 1) {
            alert("Player One Wins")
        }
        else if (gameOver == 2) {
            alert("Player Two Wins")
        }
        else {
                alert('Ball ID: ' + id + '\nPosition: (' + cx + ', ' + cy + ')');
            }
    // });
}
    



function setDrawing (svg) {

    function velocity(e) {

        // change vel calc
        let endPoint = objMousePosSVG(e);

        let vel = {}

        vel.x = -(endPoint.x - cueX) * 9;
        vel.y = -(endPoint.y - cueY) * 9;

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
        objLine.x1 = mPos.x;
        objLine.y1 = mPos.y;
        cueX = objLine.x1;
        cueY = objLine.y1;
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

    function postCalVel(data) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/calcVel',
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify ({
                    velX: data.x,
                    velY: data.y
                }),
                success: function(response, status) {
                    resolve(response)
                },
                error: function (xhr, status, error) {
                    alert("postCalcVel ERROR: " + error)
                    reject(error); // Reject the promise on error
            }
            });
        });
    }

    function getSVGs() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/svgFiles',
                type: 'GET',
                dataType: 'html',
                success: function(response){

                    var splitString = response.split(":,:");
                    var index = 0;

                    function displayPart() {
                        if(index < splitString.length)
                        {
                            $('#poolTable').html(splitString[index]);
                            if(index == splitString.length - 1)
                            {
                                resolve(splitString[index])
                            }

                            index++;
                            setTimeout(displayPart, 15);
                        }
                    }
                    displayPart();
                },
                error: function(xhr, status, error) {
                    alert("getSVG get Error : " +  error);
                    // Optionally, you can display an error message to the user
                    reject(error)
                }
            });
        })
        
    }

    function writeNewStarter(stringSVG) {
        $.ajax({
                url: '/writeStarter',
                type: 'POST',
                dataType: 'html',
                data: stringSVG,
                success: function(response) {
                    // alert("Success: " + response)
                    $('#poolTable').html(response);

                },
                error: function(status, error){
                    alert(stringSVG)
                    alert('postWrite Error: ', status, error);
                }
            })
    }

    var pOneRangeAdded = false;
    var pTwoRangeAdded = false;
    function highLow() {
        $.ajax({
            url: '/highLow',
            type: 'POST',
            contentType: 'application/json',
            success: function(response) {
                // alert("HIT")
                var pOneRange = response.pOneRange;
                var pTwoRange = response.pTwoRange;

                if (!pOneRangeAdded) {
                    $("#pOneName").append(" - " + pOneRange);
                    pOneRangeAdded = true; // Set the flag to true to prevent future updates
                }

                // Check if the range has already been added for player 2
                if (!pTwoRangeAdded) {
                    $("#pTwoName").append(" - " + pTwoRange);
                    pTwoRangeAdded = true; // Set the flag to true to prevent future updates
                }

                // alert("One: " + pOneRange + "\nTwo: " + pTwoRange)
            }, 
            error: function(error, status) {
                alert("Error in highLow:", error, "Status:", status)

            }

        })
    }

    function isGameOver(num) {
        $.ajax({
            url: '/gameOver',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({num: num}),
            success: function(response) {
                gameOver = response.num
                // alert(response.num)
                // alert(gameOver)
            },
            error: function(error, status) {
                alert("ERROR")
            }
        })
    }

    svg.addEventListener("mouseup", (e) => 
    {
        var num = 0
        if(lineEl)
        {   
            lineEl.remove();
            lineEl = null
            let distanceVel = velocity(e);

            postCalVel( {x: distanceVel.x, y: distanceVel.y} )       
            .then(response => {
                getSVGs().then(lastPart => {
                    highLow();
                    writeNewStarter(lastPart);
                    $('#poolTable').css('zIndex', 1); // Use .css method to change z-index
                    $('#lines').css('zIndex', -1);
                    isGameOver(num)
                    
                }).catch(error => {
                    alert("writeSVGStarter Error: ",+ error);
                });
            })
            .catch(error => {
                alert("getSVG ERROR: " + error)
            });
            
            lineEl = null;
            objLine = {};
        }
    });

    svg.addEventListener("mouseout", (e) => 
    {
        // if(lineEl)
        // {   
        //     lineEl.remove();
        //     let distanceVel = {}
        //     distanceVel = velocity(e);
        //     distance = distanceVel;

        //     $.ajax({
        //         url: '/calcVel',
        //         type: 'POST',
        //         contentType: "application/json",
        //         data: JSON.stringify ({
        //             velX: distanceVel.x,
        //             velY: distanceVel.y
        //         }),
        //         sucsess: function(data, status) {
        //             // alert("Data: " + data + "\nStatus: " + status);
        //         }
        //     });

        //     document.getElementById('poolTable').style.zIndex = -1;
        //     document.getElementById('lines').style.zIndex = 1;
        //     // alert("Distance:\n x: " + distance.x + " |  y: " + distance.y);
            

        //     // newSVG();
        //     lineEl = null;
        //     objLine = {};
        // }
    });
}   
    // // code snippet credited to [https://stackoverflow.com/questions/53847463/i-am-drawing-line-using-svg-and-jquery-ui-i-want-to-draw-it-in-all-directions-bu]
    // // as I took heavy inspiration on how to create and draw a line from it
    



});

// });

    


