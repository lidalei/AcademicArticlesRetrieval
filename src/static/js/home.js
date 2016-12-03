/**
 * file name: home.js
 * time: Oct. 27, 2015
 * @author Dalei Li
 */

$(function() {
	
	global_feedback_list = {relevant:[], non_relevant: []};
	
	// default vector space retrieval
	$("#user_input").keydown(function(e) {
		if (e.which == 13) {
			$("#search_articles").trigger('click');
			e.preventDefault();
		}
		else if(e.which == 32) {
			input_content = $("#user_input")[0].value;
			// query expansion
			$.ajax({
				url: '/queryExpansion/' + input_content,
		        timeout: 5000, // in milliseconds
		        success: function(response) {
					if(jQuery.type(response) == "string") {
						response = eval('(' + response + ')')
					}
					if(response.queries.length != 0) {
						$("#user_input").autocomplete({source: response.queries});
					}
		        }
			});
		}
	});
	
	
	// vector space retrieval
	$("#search_articles").click(function() {
		input_content = $("#user_input")[0].value;
		if (input_content == "" || input_content == undefined) {
			alert("Please input sth.");
			return;
		}
		$.post("/collectionVSR/" + input_content, function(response) {
				if (jQuery.type(response) == "string") {
					relevant_articles = eval("(" + response + ")");
				}
				else {
					relevant_articles = response
				}
				$("#retrieval_info").text("Vector Space Search: about " + relevant_articles.time + "s." + " About " + relevant_articles.length + " articles.");
				$("#relevant-articles").html(relevant_articles.articles);
		});
	});
	
	// prob_search_articles
	$("#prob_search_articles").click(function() {
		input_content = $("#user_input")[0].value;
		if (input_content == "" || input_content == undefined) {
			alert("Please input sth.");
			return;
		}
		$.post("/probabilisticSearch/" + input_content, function(response) {
				if (jQuery.type(response) == "string") {
					relevant_articles = eval("(" + response + ")");
				}
				else {
					relevant_articles = response
				}
				$("#retrieval_info").text("Probabilistic Search: about " + relevant_articles.time + "s." + " About " + relevant_articles.length + " articles.");
				$("#relevant-articles").html(relevant_articles.articles);
		});
		
	});
	
	
	// Boolean IR
	$("#expert_mode").click(function() {
		
		input_content = $("#user_input")[0].value;
		if (input_content == "" || input_content == undefined) {
			alert("Please input sth.");
			return;
		}
		$.post("/booleanIR/" + input_content, function(response) {
				if (jQuery.type(response) == "string") {
					relevant_articles = eval("(" + response + ")");
				}
				else {
					relevant_articles = response
				}
				$("#retrieval_info").text("Boolean Search: about " + relevant_articles.time + "s." + " About " + relevant_articles.length + " articles.");
				$("#relevant-articles").html(relevant_articles.articles);
		});
		
		
	});
	
	// feedback
	$("#relevant-articles").delegate(".dropdown-menu > li", "click", function() {
		feed_type = $(this).find(":first-child").text();
		if(feed_type == 'Relevant' && $(this).next().find(":first-child").text() == 'Non relevant') {
			global_feedback_list.relevant.push($(this).parent().parent().attr("id"));
			$(this).next().remove();
			if(global_feedback_list.relevant.length + global_feedback_list.non_relevant.length == 1) {
				$("#relevant-articles .dropdown-menu").append('<li class="btn_feedback_submit"><a href="#">Submit</a></li>');
				$(".btn_feedback_submit").click(function() {
					$.post("/relevanceFeedback/", JSON.stringify({'query': $("#relevant-articles tbody").attr('id'), 'relevant': global_feedback_list.relevant,
						'non_relevant': global_feedback_list.non_relevant}), function(response){
						
						if (jQuery.type(response) == "string") {
							relevant_articles = eval("(" + response + ")");
						}
						else {
							relevant_articles = response
						}
						
						$("#user_input").val(relevant_articles.query)
						$("#retrieval_info").text("Vector Space Search: about " + relevant_articles.time + "s." + " About " + relevant_articles.length + " articles.");
						$("#relevant-articles").html(relevant_articles.articles);
						
						global_feedback_list = {relevant:[], non_relevant: []};
				    });
				});
			}
		}
		else if(feed_type == "Non relevant"  && $(this).prev().length > 0) {
			global_feedback_list.non_relevant.push($(this).parent().parent().attr("id"));
			$(this).prev().remove();
			if(global_feedback_list.relevant.length + global_feedback_list.non_relevant.length == 1) {
				$("#relevant-articles .dropdown-menu").append('<li class="btn_feedback_submit"><a href="#">Submit</a></li>');	
			}
		}
	});
	
	// search authors
	$("#search_authors").click(function() {
		input_content = $("#user_input")[0].value;
		window.open('/getArticlesByAuthor/' + input_content, "_self ");
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