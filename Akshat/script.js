var socket = io.connect();
socket.on("receiveData", function(message) {
    document.getElementById("text-box").innerText = message;
});

document.getElementById("send-btn").addEventListener('click', clickButton);

function clickButton() {
    console.log("button clicked");
    let inputBox = document.getElementById("input-box");
    inputBox.value = "";
    socket.emit("input", inputBox.value);
}