
//NOTES!!: 
//perhaps we could have a dict on client side with actual hard names and have ids be key vals? user accesibility or whatnot if we are keeping this soley txt based
//assigning player 1,2,3,4 etc. (something in the begining to send to each player which # they are, and also something to send updates on whose turn it is)
//how many cards does each player have left??
//tested it and got top card wild on first go : fix this 
//ask about unplayable also transfer it lol

//basic set up stuff

var socket = io.connect('http://127.0.0.1:5000');
currenthand=[];
poolcard=""; 

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

	console.log("game displayed"); 
	$(messages).empty();

	var header=$("#topcard");
	header.show();
	header.html("");

	var pheader=$("#playerheader"); 
	pheader.show(); 

	var box= $("#game"); 
	box.innerHTML="";

	var notif = $("#notif");
	notif.show();

	var command =$("#input"); 
	command.show(); 
	
	var cturn= $('#currentturn')
	cturn.show(); 

}); 

socket.on('playernum', function(num){
	console.log('NUM WAS REV')
	var pheader=document.getElementById("playerheader"); 
	pheader.innerText="YOUR CARDS (PLAYER "+ num +" ): \n"; 

});



//displays the players' hands also processes whether or not the user needs to draw bc they have no more avaliable cards 
socket.on('hand', function(cards){
	console.log('hand was recv'); 
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

	var command = $("#input"); 
	len = currenthand.length; 
	
	button.on('click', function() {
		var played = false;
		while(!played) {
			var input = Number(command.val()); 
			//insert something that actually checks if its actually a num 
			if (input < 0 || input >= l){
				set_notif("That isn't a valid card number! Please enter a number corresponding to the cards in your hand!"); 	
			}
			else if (!playable(currenthand[input])){
				set_notif("This card isn't playable :( Please choose another card!");
			}	
			else {
				emit('play',currenthand[input]); 
				played = true;
			}
		}
		
	});

});


//function to set notif bc it's annoying to rewrite this code 
function set_notif (message) {
	var notif= document.getElementById("notif"); 
	notif.innerText=message;
}

// should be good
function playable(card, pool) {
	playable = false;
	card = card.split(" ");
	pool = pool.split(" ");
	
	if (card[3] == 'wild') {
		playable = true;
	}

	if (pool[0] == '1' && card[0] == '1' && pool[3] == card[3]) {
		playable = true;
	}

	for (var i = 1; i < 2; ++i) {
		if (card[i] == pool[i]) {
			playable = true;
		}
	}
	
	return playable; 
} 
