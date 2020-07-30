
//NOTES!!: 
//perhaps we could have a dict on client side with actual hard names and have ids be key vals? user accesibility or whatnot if we are keeping this soley txt based
//assigning player 1,2,3,4 etc. (something in the begining to send to each player which # they are, and also something to send updates on whose turn it is)
//how many cards does each player have left??
//tested it and got top card wild on first go : fix this 
//ask about unplayable also transfer it lol

//basic set up stuff

var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function () {
	console.log("socket connected")
});

socket.on('join_room', function (msg) {
	console.log("joined room")
});

socket.on('message', function(msg) {
	$("#messages").append('<li>'+msg+'</li>');
	console.log('Received message');
});

//code for when the game starts 


socket.on('game_display', function(){

	$(messages).empty();

	var header=$("#topcard");
	header.show();

	var pheader=$("#playerheader"); 
	pheader.show(); 

	var box= $("#game"); 
	box.html="";

	var notif = $("#notif");
	notif.show();

	var command =$("#input"); 
	command.show(); 

	var button= $("#sendbutton")
	button.show(); 
	button.on('click',function(){
		var input= command.val(); 
		alert(input);
	});

	var cturn= $('#currentturn')
	cturn.show(); 

}); 

socket.on('playernum', function(num){
	var pheader=document.getElementById("playerheader"); 
	pheader.innerText="YOUR CARDS (PLAYER "+ num +" ): \n"; 

});

//displays the players' hands 
socket.on('hand', function(cards){
	var box= document.getElementById("game"); 
	box.innerHTML=""; 
	for(i=0; i<cards.length;i++)
		box.innerText+= i + " " + cards[i] +"\n"; 
	set_notif("What card would you like to play? (please send in the corresponding number)"); 
});

//displays top card to all players 
socket.on('pool', function(pcard){
	var header=document.getElementById("topcard");
	header.innerText= "top card: " + pcard; 
});

//show whose turn it currently is 
socket.on('turn', function(num){
	turn=num+1;
	var tnum= document.getElementById("currentturn"); 
	tnum.innerText= "Player " + turn + "'s Turn!"
});

//function to set notif bc it's annoying to rewrite this code 
function set_notif (message){
	var notif= document.getElementById("notif"); 
	notif.innerText=message; 
}



	
