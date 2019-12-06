function validatePassword(){
	var passwd = document.getElementById('passwd').value;
	var confirm_passwd =document.getElementById('confirm_passwd').value;

	if(passwd == confirm_passwd){
		document.getElementById('passwd_status').innerHTML = "<p class = 'green-text'>Password Validation Successful</p>";
	}
	else if(passwd != confirm_passwd){
		document.getElementById('passwd_status').innerHTML = "Password Mismatch!!!";
	}
	else if(passwd == '' && confirm_passwd ==''){
		document.getElementById('passwd_status').innerHTML = "Password is empty";
	}
	else{
		console.log('No password validation required')
	}
}
function validator(){
	setInterval(validatePassword, 300)
}