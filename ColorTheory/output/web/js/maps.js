/*
# Maps module for Color Theory analysis
by Vicente Yanez, November 2015

This module gets the data from the html document to map the color information into the HSV and the CIE xy maps as HTML5 canvas elements.

### Contents
**Global variables**
* *allPalettes*, get the array of all color palettes (0 if there is just one as in the detailed view)
* *saturation (Image)*, saturation-hue circle for canvas drawing
* *huevalue (Image)*, hue-value stripe for canvas drawing
* *cromaticity (Image)*, CIE xy cromaticity map for canvas drawing

 */

 // We get the container to look at
var allPalettes = document.getElementsByClassName("container");

// These images will be drawn on the canvas, they are the background of them
var saturation = new Image();
var huevalue = new Image();
var cromaticity = new Image();

// Here I'm making sure that the images have been loaded before doing anything else
cromaticity.onload = function(){
    saturation.src = "../img/sat.png";    
}

saturation.onload = function(){
    huevalue.src = "../img/hue_val.png";
}

// Once we are done, we can draw everything
huevalue.onload = function(){
    // This is to verify if we are on a simple layout (with a bunch of palettes) or a detailed one (with a single palette)
    if(allPalettes.length == 0){
        drawCanvas(0);
    }else{
        // If it is a simple layout, we iterate through all of the palettes found
        for(i=0; i < allPalettes.length; i++){
            drawCanvas(i);
        }
    }
}

cromaticity.src = "../img/CIE1931xy.png";

// Function to get the canvases from the html and draw the backgrounds
// when done, call to draw each one of the marks on the canvas
function drawCanvas(index){
    var canvas_hs;
    var canvas_cie;
    
    // Retrieve the canvas from doc
    canvas_hs = getCanvas("map", index);
    canvas_cie = getCanvas("cromaticity", index);

    // Get the 2d context from the canvas
    var context_hs = canvas_hs.getContext('2d');
    var context_cie = canvas_cie.getContext('2d');
    
    // Draw all backgrounds
    size = putBackground("saturation", saturation, context_hs, canvas_hs);
    putBackground("huevalue", huevalue, context_hs, canvas_hs);
    putBackground("cromaticity", cromaticity, context_cie, canvas_cie);

    // Draw the marks
    drawMarks(index, size, context_hs, canvas_hs, context_cie, canvas_cie)
}

function drawMarks(index, sat_size, context_hs, canvas_hs, context_cie, canvas_cie){
    var palette;

    // If it is a detailed view (with a single palette), we get it
    if(allPalettes.length == 0){
        palette = document.getElementsByClassName("palette")[0];
    // If not, get the palette from the container based on the index
    }else{
        palette = document.getElementsByClassName("container")[index].getElementsByClassName("palette")[0];
    }
    // Finally, get the color information from the doc
    var colors = palette.getElementsByClassName("color-info");

    var i;
    var old_x_hv = -1;
    var old_y_hv = -1;
    
    var old_x_sat = -1;
    var old_y_sat = -1;
    var start_x_sat = -1;
    var start_y_sat = -1;
    
    var old_x_cie = -1;
    var old_y_cie = -1;


    // the radius for the saturation
    r = sat_size/2;
    // the x coord corresponding to the center of the circle 
    c = canvas_hs.width / 2;
    // the y coord corresponding to the center of the circle 
    k = sat_size / 2;

    // height of the huevalue stripe
    hueval_height = canvas_hs.width/4;
    // base y for saturation circle coordinates conversion
    y = canvas_hs.height - hueval_height;

    // coordinates x,y corresponding to the origin of the cromaticity map
    cie_axis_x = canvas_cie.width * 0.83;
    cie_axis_y = canvas_cie.height * 0.87;
    
    cie_xo = canvas_cie.width * 0.12;
    cie_yo = canvas_cie.height - ( canvas_cie.height * 0.1 );

    for (i=0; i<colors.length; i++){
        // Get the HSV, ciex and ciey values from the table associated with this color
        var hsv = colors[i].getElementsByTagName("table")[0].rows[2].cells[1].textContent;
        var ciex = colors[i].getElementsByTagName("table")[0].rows[5].cells[1].textContent;
        var ciey = colors[i].getElementsByTagName("table")[0].rows[6].cells[1].textContent;

        // clean formatting
        hsv = hsv.replace(/\s+/g, '');

        // extract separate values from string
        var h = hsv.substring(0, hsv.indexOf(","));
        var s = hsv.substring(hsv.indexOf(",") + 1, hsv.lastIndexOf(","));
        var v = hsv.substring(hsv.lastIndexOf(",") + 1, hsv.length);

        // HUEVAL CALCS
        // We have to calculate x and y coordinates of the mark to be drawn based on the hue and value from the html
        // we map the hue (0-360 degrees) to a single line
        var px = h * canvas_hs.width / 360;
        // and then we map the value within the stripe
        var py = y + hueval_height - (v * hueval_height / 100);

        // if we had a mark before, we draw the line from there to this new position
        if(old_x_hv != -1 && old_y_hv != -1){
            putLine(old_x_hv, old_y_hv, px, py, context_hs);
        }

        // we put the mark
        putMark(px, py, i, context_hs);

        // and save coords for next iteration
        old_x_hv = px;
        old_y_hv = py;

        // SATURATION CALCS
        // We have to calculate x and y coordinates of the mark to be drawn based on the hue and saturation from the html

        // Trigonometrically... 
        // We have the angle from the origin (hue), and the hipotenuse of the triangle is the saturation
        // if we map the saturation within the size of the circle using cos and sin, we can get the proper
        // coords for the mark
        px = c + ( Math.cos( toRadians(h) ) * (s * r / 100) );
        py = k + (-1) * ( Math.sin( toRadians(h) ) * (s * r / 100) );

        // if we had a mark before, we draw the line from there to this new position
        if(old_x_sat != -1 && old_y_sat != -1){
            putLine(old_x_sat, old_y_sat, px, py, context_hs);
        }

        // if this is the first one, we save it to close the loop
        if(i == 0){
            start_x_sat = px;
            start_y_sat = py;
        }
        
        // we put the mark
        putMark(px, py, i, context_hs);

        // and save coords for next iteration
        old_x_sat = px;
        old_y_sat = py;

        // CROMATICITY CALCS
        // This mark is more straigh forward since the x and y coords are already calculated
        px = cie_xo + ( ciex * cie_axis_x / 0.8 );
        py = cie_yo - ( ciey * cie_axis_y / 0.9 )

        // if we had a mark before, we draw the line from there to this new position
        if(old_x_cie != -1 && old_y_cie != -1){
            putLine(old_x_cie, old_y_cie, px, py, context_cie);
        }

        // we put the mark
        putMark(px, py, i, context_cie);

        // and save coords for next iteration
        old_x_cie = px;
        old_y_cie = py;

    }

    // finally we close the loop
    putLine(old_x_sat, old_y_sat, start_x_sat, start_y_sat, context_hs);
}

function getCanvas(type, index){
    var result;
    result = document.getElementsByClassName(type)[index].getElementsByTagName("canvas")[0];
    return result;
}

function putBackground(type, img, context, canvas){
    var result;
    var w;
    var h;
    var x;
    var y;
    
    if(type == "saturation"){
        var size = canvas.width * 0.7;
        w = size;
        h = size;
        x = canvas.width / 2 - size / 2;
        y = 0;
        result = size;
    }else if(type == "huevalue"){
        w = canvas.width;
        h = w/4;
        x = 0;
        y = canvas.height - h;
    }else if(type == "cromaticity"){
        w = canvas.width;
        h = canvas.height;
        x = 0;
        y = 0;
    }
    
    context.drawImage(img, x, y, w, h);
    return result;
}

function putMark(x, y, i, context){
    context.beginPath();
    context.arc(x, y, 4, 0, 2 * Math.PI, false)        
    context.fillStyle = '#CCC';
    context.fill();
    if (i == 0){
        context.strokeStyle = '#000';
    }else{
        context.strokeStyle = '#999';
    }
        context.stroke();
}

function putLine(x1, y1, x2, y2, context){
    context.beginPath();
    context.moveTo(x1, y1);
    context.lineTo(x2, y2);
    context.lineWidth = 1;
    context.strokeStyle = '#DDD';
    context.stroke();
}

function toRadians (angle){
    return angle * (Math.PI / 180);
}