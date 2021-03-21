// basic websocket client webpage made as a proof of concept
var ws = new WebSocket("ws://IP:PORT/"); // connects to websocket server            
ws.onmessage = function (event) {
                    // when server sends a message this block executes
    
    if (event.data[0] == 'T') {                
        document.getElementById("spot1").style.backgroundColor = "green";}

    else{
        document.getElementById("spot1").style.backgroundColor = "red";}

    if (event.data[1] == 'T') {                
        document.getElementById("spot2").style.backgroundColor = "green";}

    else{
        document.getElementById("spot2").style.backgroundColor = "red";}
                    
    };
