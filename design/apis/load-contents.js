// Loads contents from JSON and make links for each item
function loadContents() {
	$ajaxUtils.sendGetRequest(utils.CONTENTS_FILE, 
		function(response) {
			document.getElementById("heading-table-of-contents").textContent = "API Table of Contents";

			var contents = JSON.parse(response);

			var html = "";
			for (var i = 0; i < contents.length; i++) {
				html += "<li>" + utils.linkTo(contents[i]) + "</li>";
			}

			utils.insertHtmlById("list-table-of-contents", html);
		});
}