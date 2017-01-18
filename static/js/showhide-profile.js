$(document).ready(function() {
	$('.showhide-form').hide();
	
	$('input[type="checkbox"]').click(function() {
		if($(this).checked=true) {
			console.log("#input-{0}".format($(this).attr('id')))
			$("#input-{0}".format($(this).attr('id'))).show();
		}
		if($(this).checked=false) {
			$("#input-{0}".format($(this).attr('id'))).hide();
		}
	});
});