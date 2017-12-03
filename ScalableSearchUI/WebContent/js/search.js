$(document).ready(function(){
	
	$("#txtSearch").keypress(function(e) {
	    if(e.which == 13)
	    	$("#btnSearch").click();
	});
	
	$("#btnSearch").click(function(){
		$("#searchResults").html($("#loadingImage").html());
		
		var postData = "queryString="+$("#txtSearch").val();
		$.ajax({
			url: "AJAXSearch",
			data: postData
		})
		.done(function(data){
			resultData = JSON.parse(data);
			if(resultData.articleList.length==0)
				$("#searchResults").html("")
								   .append(
										   $("<div>").addClass("alert alert-danger")
										   			 .html("No Matching Documents Found!")
										  );
			else{

				var resultElem = $("<ul>").addClass("list-group");
				
				var aList = resultData.articleList;
				
				$(aList).each(function(i, article){
					$(resultElem).append(
						$("<li>").addClass("list-group-item")
						   .append(
							   $("<h4>").addClass("article-header")
							   			.html("Result " + (i+1))
						   )
						   .append(
							   $("<p>").addClass("article-body")
							   		   .html(article[1])
						   )
					);
				});
				
				console.log(resultElem)
				$("#searchResults").html("")
								   .append(
										   $("<div>").addClass("alert alert-success")
										   			 .html("Returned "+ aList.length + " articles.")
										  )
								   .append(resultElem);
			}
		});
	});
});