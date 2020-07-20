var socket = io.connect();
console.log("Hello world");
socket.emit("join");