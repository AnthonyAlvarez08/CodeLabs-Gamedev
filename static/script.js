
//NOTES!!: 
//perhaps we could have a dict on client side with actual hard names and have ids be key vals? user accesibility or whatnot if we are keeping this soley txt based
//assigning player 1,2,3,4 etc. (something in the begining to send to each player which # they are, and also something to send updates on whose turn it is)
//how many cards does each player have left??
//tested it and got top card wild on first go : fix this 
//ask about unplayable also transfer it lol

//basic set up stuff

var socket = io.connect();
var currenthand=[]; 
var poolcard=""; 

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


	var cturn= $('#currentturn')
	cturn.show(); 

}); 

socket.on('playernum', function(num){
	var pheader=document.getElementById("playerheader"); 
	pheader.innerText="YOUR CARDS (PLAYER "+ num +" ): \n"; 

});

//displays the players' hands 
socket.on('hand', function(cards){
	currenthand=cards; 
	var box= document.getElementById("game"); 
	box.innerHTML=""; 
	for(i=0; i<cards.length;i++)
		box.innerText+= i + " " + cards[i] +"\n"; 
	set_notif("What card would you like to play? (please send in the corresponding number)"); 
});

//displays top card to all players 
socket.on('pool', function(pcard){
	poolcard=pcard;
	var header=document.getElementById("topcard");
	header.innerText= "top card: " + pcard; 
});

//show whose turn it currently is 
socket.on('turn', function(num){
	turn=num+1;
	var tnum= document.getElementById("currentturn"); 
	tnum.innerText= "Player " + turn + "'s Turn!"
});

//hides the send button thus 'locking' a player 
socket.on('lock', function() {
	var button= $("#sendbutton"); 
	button.hide(); 
});

//shows the send button/ 'unlock's' the player and takes in the first input as a num & sends a play signal if valid 
socket.on('unlock', function() {

	var button = $("#sendbutton"); 
	button.show(); 
/*
	var command = $("#input"); 
	len = currenthand.length; 
	played=false;
	
	while(!played){
		button.on('click',function(){
			var input= (command.val()); 
			if(Number.isInteger(input)) {
				//insert something that checks if it's actually a num
				if((input >= 0 && input < len)) {
					if(playable(currenthand[input], poolcard)) {
						socket.emit('play',{cid:currenthand[input],hand:currenthand});
						played=true;
						console.log("played a card");
					}
					else {
						set_notif("That isn't a valid card number! Please enter a number corresponding to the cards in your hand!");
					}
				} else {
					set_notif("That isn't a valid card number! Please enter a number corresponding to the cards in your hand!");
				}
			} else {
				set_notif("Please enter a valid card number");
			}
		});		
		
	}
	*/


});

//function to set notif bc it's annoying to rewrite this code 
function set_notif (message){
	var notif= document.getElementById("notif"); 
	notif.innerText=message; 
}



	
