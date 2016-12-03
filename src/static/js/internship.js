$(function() {
	// inspect full images
	$(".small-image").click(function() {
	var imageName = $(this).attr("id");
	var imageTitle = $(this).attr("title");
	$("#dialog").html('<img src="resources/images/internship/'+ imageName +'.png" class="fullscreen-image" id="' + imageName+ '_full_screen" alt="'+imageTitle+'" title="'+imageTitle+'"/>');
	var dialogHandler = $("#dialog").dialog({
		open:function(){$("#"+imageName+"_full_screen").click(function(){dialogHandler.dialog("close")});},
		title: imageTitle,
		width: "75%",
		position: ["10%","10%"],
		modal: true});
	});
	// scroll window to hide or show backToTop button
	$(window).scroll(function() {
		if ($(this).scrollTop() > 150) {
			$("#backToTop").fadeIn(100);
		} else {
			$("#backToTop").fadeOut(100);
		}
	});
	
	// jQuery animation scroll
	$("#backToTop").click(function(event) {
		event.preventDefault();
		$("body,html").animate({scrollTop: 0}, 500);
	});
});