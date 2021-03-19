// basic websocket client webpage made as a proof of concept
var ws = new WebSocket("ws://192.168.0.10:5678/"); // connects to websocket server            
ws.onmessage = function (event) {
                    // when server sends a message this block executes
    
    if (event.data == "True") {                
        document.getElementById("spot1").style.backgroundColor = "green";}

    else{
        document.getElementById("spot1").style.backgroundColor = "red";}
                    
    };
