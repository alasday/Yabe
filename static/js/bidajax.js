$(document).ready(function() {
	function reload() {
	    $.ajax({
		    url: "/bidajax",
			type: "GET",
			done: function(data) {
			console.log(data);
			$("#updatingElement").html(data);
		    }
	    });
	}
	setInterval(reload, 2000);
});
		   