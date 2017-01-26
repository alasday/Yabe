$(document).ready(function() {
	$.ajax({
		url: "/bidajax",
		type: "GET",
		done: function(data) {
		    $("#updatingElement").html(data);
		}
	    });
	    });
		   