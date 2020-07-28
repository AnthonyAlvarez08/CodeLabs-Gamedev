/*var socket = io.connect();
console.log("Hello world");
socket.emit("join");*/


var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function () {
	console.log("socket connected")
});

socket.on('join_room', function (msg) {
	console.log("joined room")
});




/*
** how do we send message from server side? also not sure if this works
    socket.on('receivedData', function (message) {
        document.getElementById("text-box").innerText = message;
    });
    document.getElementById("send-btn").addEventListener('click', clickButton);
    function clickButton() {
        console.log("button clicked");
        let inputBox = document.getElementById("input-box");
        inputBox.value = "";
        socket.emit('input, inputBox.value);
    }
*/
socket.on('message', function (msg) {
	$("#messages").append('<li>' + msg + '</li>');
	console.log('Received message');
});
/*
	$('#sendbutton').on('click', function() {
		socket.send($('#myMessage').val());
		$('#myMessage').val('');
	});
	*/