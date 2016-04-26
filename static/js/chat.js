$(window).load(onLoad);
$('#send').click(sendMessage);
$('#addUserButton').click(sendUser);
//$('#message').on('input',enter);
$('#message').keypress(enter);

var csrf_token = $.cookie('csrftoken');
var messages = [];
var users = [];
var loading = true;
var readSelf = false;

var tempi = 0;
var messageQueue = [];
var readIndex = 0;
var messageIndex = 0;

function enter(e){
  if( e.which == 13){
    sendMessage();
  }
}

function replay(button){
  var i = button.parentElement.querySelector('#messageData').value;
  read( messages[i] );
}

/**
 * parses messages into array of message
 */
function getMessages(string){
  if( string === undefined)
    return;
  if( string == "")
    return;

  var raw = JSON.parse( string );

  var message = {};

  for( var i = 0; i < raw.length; i++){
    var mod = i % 5;

    switch(mod){
      case 0:
        message['author'] = raw[i];
        break;
      case 1:
        message['time'] = raw[i];
        break;
      case 2:
        message['text'] = raw[i];
        break;
      case 3:
        message['id'] = raw[i];
        break;
      case 4:
        message['voice'] = raw[i];
        addMessage(message);
        break;
    }

  }

}

/**
 * parses users into array of users
 */
function getUsers(string){
  if(string === undefined)
    return;
  if( string == "")
    return;

  var raw = JSON.parse( string );
  for( var i = 0; i < raw.length; i++){
    if( users.indexOf(raw[i]) == -1 )
      addUser(raw[i]);
  }
}

/**
 * Adds message to Array and TODO:document
 * message contains
 * message['author']
 * message['time']
 * message['text']
 */
function addMessage(message){
  messages.push( $.extend(true,{},message) );

  //control for reading messages
  if( loading == false){
    if( readSelf){
      read(message);
    }
    else{
      if( message['author'].valueOf() != username.valueOf() )
        read(message);
    }
  }

  //TODO: insert message in document


  //
  /*
    $('#messageZone').append('<div id="messageBox" class="well well-sm messageBox"><label id="author" class="author">' + display_author(message) + ':&nbsp;</label><label id="content">'+ display(message)+'</label></div>');
    */
   var copy = $('#messageBox').clone();
   copy.find('#author').html( display_author(message) + ":&nbsp;" );
   copy.find('#content').html( display(message) );
   copy.find('#messageData').val(messageIndex);
   messageIndex++;
   copy.show();

   $('#messageZone').append(copy);

    updateScroll();
}

function updateScroll() {

    var count = $('#messageZone');
    $('html, body').animate({
      scrollTop: $('#end').offset().top
    }, 0);

}

function display(message) {
    var output = message['text'];
    return output;
}

function display_author(message) {
    var output = message['author'];
    return output;
}
/**
 * Adds user to Array and TODO:document
 * username
 */
function addUser(username){
  users.push(username);

  //TODO: insert user into document

    $user_list=$('#user_list');
    $user_list.append('<li>' + username + '</li>');

}

/**
 * asks server for room information
 */
function updateRoom(){
  data = {}

  sendAjax('/chatInfo/update/',data,onUpdateResponse);
}

/**
 * Called when document has been loaded
 */
function onLoad(){
  console.log("on load");
  loading = true;

  //asks server for information
  updateRoom();

  //start polling
  setTimeout(poll,1200);
}

/**
 * responds to an update response from the server
 */
function onUpdateResponse(json){
  getMessages(json.messages);
  getUsers(json.users);
}

/**
 * read a message to the user
 */
function read(message){
  if( responsiveVoice.isPlaying()){
    var temp = $.extend(true,{},message);
    messageQueue.push( temp );
    return;
  }

    responsiveVoice.speak(message['text'],message['voice'],{ onend : nextRead });
}

function nextRead(){

  if( readIndex  < messageQueue.length ){
    read( messageQueue[ readIndex ] );
    readIndex++;
  }
}

/**
 * sends a message to the chat room
 */
function sendMessage(){
  console.log("clicked");
  var message = $('#message').val();

  data = { 'message' :  message };
  sendAjax('/chatInfo/sendMessage/',data,onSendMessageResponse);
}

/**
 * sends a user info
 */
function sendUser(){
  console.log("clicked");
  var username = $('#user_name').val();

  data = { 'username' :  username };
  sendAjax('/chatInfo/sendUser/',data,onSendUserResponse);
}

/**
 * responds to response from sending message to server
 */
function onSendMessageResponse(json){
  console.log("send message success");
  if( !json.errors){
    onUpdateResponse(json);
    $('#message').val("");
  }
  else{
    console.log("error");
    console.log(json);
  }

}

/**
 * responds to response from sending username to server
 */
function onSendUserResponse(json){
  console.log(json);
  if( json.errors) {
    var errorlist = JSON.parse(json.errors);
    for(i = 0; i < errorlist.length; i++) {
      if(errorlist[i] == 3){
        $("#userNotExists").show();
        $("#usernameEmpty").hide();
        $("#userInRoom").hide();
      }
      else if(errorlist[i] == 4){
        $("#userNotExists").hide();
        $("#usernameEmpty").show();
        $("#userInRoom").hide();
      }
      else if(errorlist[i] == 8){
        $("#userNotExists").hide();
        $("#usernameEmpty").hide();
        $("#userInRoom").show();
      }
    }
  }
  else{
    $("#userNotExists").hide();
    $("#usernameEmpty").hide();
    $("#userInRoom").hide();
    $("#addUserModal").modal("hide");
    console.log("success");
  }
}

/**
 * adds csrf token to ajax and sends data to url, and response goes to successCall
 */
function sendAjax(url,data,successCall){

  lastMessage = messages[ messages.length - 1];
  if( lastMessage === undefined)
    lastMessage = 0;
  else
    lastMessage = lastMessage['id'];

  console.log("lastMessage" + lastMessage);

  data['lastMessage'] = lastMessage;
  data['room'] = title;
  data['csrfmiddlewaretoken'] = csrf_token;
  $.ajax({url: url, type: "POST", data: data, success: successCall, error: responseFailure});
}

/**
 * poll the server for more information
 */
function poll(){
  //console.log("poll" + tempi);
  tempi++;
  loading = false;

  updateRoom();

  setTimeout(poll,800);
}

/**
 * This is called when the client fails to connect to the server
 */
function responseFailure(json){
  console.log("responseFailure");
  console.log(json);
}
