//format function from a kind soul on stack overflow
String.prototype.format = function() {
  var str = this;
  for (var i = 0; i < arguments.length; i++) {       
    var reg = new RegExp("\\{" + i + "\\}", "gm");             
    str = str.replace(reg, arguments[i]);
  }
  return str;
}

$(document).ready(function() {
	$('.showhide-form').hide();
	
	$('input[type="checkbox"]').click(function() {
		$("#input-{0}".format($(this).attr('id'))).toggle();
		/*
		if($(this).checked=false) {
			$("#input-{0}".format($(this).attr('id'))).hide();
		}
		else {
			$("#input-{0}".format($(this).attr('id'))).show();
		}
		*/
	});
});