var socket = io();


// Event handler for new connections.
// The callback function is invoked when a connection with the
// server is established.
socket.on('connect', function() {
    socket.emit('my_event', {data: 'I\'m connected!'});
});

socket.on('cheese', function(value) {
    console.log(value.data);
    document.getElementById("cheese").innerHTML = value.data;
    
});
socket.on('meat', function(value) {
    console.log(value.data);
    document.getElementById("meat").innerHTML = value.data;
    
});
socket.on('vegetable', function(value) {
    console.log(value.data);
    document.getElementById("vegetable").innerHTML = value.data;
    
});
socket.on('bread', function(value) {
    console.log(value.data);
    document.getElementById("bread").innerHTML = value.data;
    document.getElementById("bread1").innerHTML = value.data;
    
});
socket.on('response', function(value) {
    console.log(value.data);
    document.getElementById("ai").innerHTML = value.data;
    
});


function buttonClicked() {
    console.log('Button clicked!');
    socket.emit('generate', {data: 'button pressed'});
    console.log("Button pressed");

    setTimeout(function () {
        // location.reload();
    }, 3000);
}

// function reloadPage() {
//     // Reload the page if the video fails to load
//     setTimeout(function () {
//         location.reload();
//         }, 2000); // 2000 milliseconds = 2 seconds
        
// }