// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function messageSender(){
	let mail = document.getElementById('mail').value;
	let posted_by = document.getElementById('posted_by').value;
	let message = document.getElementById('content').value;

	console.log(mail);
	console.log(posted_by);
	console.log(message);

if (window.XMLHttpRequest) {
    // code for modern browsers
    messenger = new XMLHttpRequest();
    messenger.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
  	// Ready code here
  	console.log("Message successfully delivered")
};
    messenger.open("POST", "/home/message", true);
    messenger.setRequestHeader('X-CSRFToken', csrftoken);
    messenger.setRequestHeader("Content-Type", "application/json");
    let sendmessage = {"mail": mail,"posted_by":posted_by,"message":message}
    messenger.send(JSON.stringify(sendmessage));}}
else {
    // code for old IE browsers
    messenger = new ActiveXObject("Microsoft.XMLHTTP");
}

}


/*
function contentReceiver(){

if (window.XMLHttpRequest) {
    // code for modern browsers
    messenger = new XMLHttpRequest();
    messenger.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
  	// Ready code here
  	var reply = JSON.parse(this.responseText);
  	document.getElementById('demo').innerHTML = 'My name is '+ reply.name + ' i left @ '+ reply.age +'.'
  }
};
    messenger.open("POST", "/home/message", true);
    messenger.setRequestHeader('X-CSRFToken', csrftoken);
    messenger.setRequestHeader("Content-Type", "application/json");
    let g = {'name':'Gbenga','age':15}
    let f = {name:"John Rambo", time:"2pm"}
    messenger.send(JSON.stringify(g));
 } else {
    // code for old IE browsers
    messenger = new ActiveXObject("Microsoft.XMLHTTP");
}

}
*/

/*
function testActiveKey() {
document.addEventListener('keydown', (event) => {
	const Keyname = event.key;
	if(Keyname){
		return true
	}
});
};

function testCurrentKeyState(){
	var g = testActiveKey();
}

setInterval(testActiveKey,3000);
var g = new KeyboardEvent();
console.log(g.KeyCode)
*/

var timeoutID;
 
function setup() {
    this.addEventListener("keypress", resetTimer, false);
 
    startTimer();
}
setup();
 
function startTimer() {
    // wait 2 seconds before calling goInactive
    timeoutID = window.setTimeout(goInactive, 7000);
}
 
function resetTimer(e) {
    window.clearTimeout(timeoutID);
 
    goActive();
}
 
function goInactive() {
    // do something
    var output = document.getElementById("theUrl").innerHTML;
    window.location.href = output;
}
 
function goActive() {
    // do something
         
    startTimer();
}