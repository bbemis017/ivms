$(window).load(onLoad);
$('#send').click(sendMessage);
$('#addUserButton').click(sendUser);

var csrf_token = $.cookie('csrftoken');
var messages = []
var users = []

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
    if( i % 3 == 0){
      message['author'] = raw[i];
    }
    else if( i % 3 == 1)
      message['time'] = raw[i];
    else{
      message['text'] = raw[i];
      addMessage(message);
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
  messages.push(message);

  //TODO: insert message in document
    $('#messageZone').append('<div id="messageBox" class="well well-sm messageBox"><label id="author" class="author">' + display_author(message) + ':&nbsp;</label><label id="content">'+ display(message)+'</label></div>');
}

function updateScroll() {
/*
    var element = document.getElementById("messageZone");
    element.scrollTop = element.scrollHeight;
*/
    var $count = $('#messageZone');
    $count[0].scrollTop = $count[0].scrollHeight;

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
    $user_list.append('<li>' + users[0] + '</li>');

}

/**
 * asks server for room information
 */
function updateRoom(){
  sendAjax('/chatInfo/update/',{},onUpdateResponse);
}

/**
 * Called when document has been loaded
 */
function onLoad(){
  console.log("on load");

  //asks server for information
  updateRoom();
}

/**
 * responds to an update response from the server
 */
function onUpdateResponse(json){
  console.log("update response");
  getMessages(json.messages);
  console.log(messages);
  getUsers(json.users);
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
  if( !json.errors)
    onUpdateResponse(json);
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
  data['room'] = title;
  data['csrfmiddlewaretoken'] = csrf_token;
  $.ajax({url: url, type: "POST", data: data, success: successCall, error: responseFailure});
}

/**
 * This is called when the client fails to connect to the server
 */
function responseFailure(json){
  console.log("responseFailure");
  console.log(json);
}
