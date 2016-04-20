$(window).load(pageLoaded);

function pageLoaded() {
	var voicelist = responsiveVoice.getVoices();
        for(var i = 0; i < voicelist.length; i++) {
		addOption(voicelist[i].name);	
	}
}

function addOption(voice) {
	var option = $("#select").clone();
	option.html(voice);
	option.attr("value", voice);
        $("#voice").append(option);
		
}

