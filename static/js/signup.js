$(window).load(pageLoaded);

function pageLoaded() {
	var voicelist = responsiveVoice.getVoices();
    for(var i = 0; i < voicelist.length; i++) {
		addOption(voicelist[i].name);	
	}
    if( voice !== undefined){
      $('#voice').val(voice);
    }
}

function addOption(voice) {
	var option = $("#select").clone();
	option.html(voice);
	option.attr("value", voice);
        $("#voice").append(option);
		
}

function replaceSpaces(){
  var name = $('#room_name').val();
  name = name.replace(" ","_");
  $('#room_name').val(name);
}

