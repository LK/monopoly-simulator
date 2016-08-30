// Loads an API of the given name into the content
function loadAPI(objName) {
	// Constants
	var CLASS_NAME 				= "'name'";
	var CLASS_TYPE 				= "'type'";
	var CLASS_DESCRIPTION 		= "'description'";
	var CLASS_ARGUMENTS			= "'arguments'";
	var CLASS_DEFAULT 			= "'default'";
	var CLASS_RETURN_TYPE		= "'return-type'";
	var CLASS_ACCESS			= "'access'";
	var CLASS_OVERRIDES			= "'overrides'";
	var CLASS_HEADING_SECTION 	= "'heading-section'";

	var HTML_NONE				= "<p>None</p>";

	// Returns the HTML that inflates the constants for this API
	function inflateConstants(constants) {
		if (constants.length == 0) {
			return HTML_NONE;
		}

		var html = "";
		for (var i = 0; i < constants.length; i++) {
			var name 		= constants[i].name;
			var type 		= constants[i].type;
			var description = constants[i].description;
			html += "<li>";
			html += "<h3 class=" + CLASS_NAME + ">" + utils.monospace(name) + "</h3>";
			html += "<ul>"; // sub-list everything under constants[i].name

			html += "<li><span class=" + CLASS_TYPE + ">" + utils.monospace(utils.linkTo(type)) + "</span></li>";
			html += "<li class=" + CLASS_DESCRIPTION + ">" + description + "</li>";
			html += "</li>";

			html += "</ul>"; // close sub-list
		}
		return html;
	}

	// Returns the HTML that inflates the instance variables for this API
	function inflateInstanceVariables(instanceVariables) {
		if (instanceVariables.length == 0) {
			return HTML_NONE;
		}

		var html = "";
		for (var i = 0; i < instanceVariables.length; i++) {
			var name 		= instanceVariables[i].name;
			var type 		= instanceVariables[i].type;
			var description = instanceVariables[i].description;
			html += "<li>";
			html += "<h3 class=" + CLASS_NAME + ">" + utils.monospace(name) + "</h3>";
			html += "<ul>"; // sub-list everything under constants[i].name

			html += "<li><span class=" + CLASS_TYPE + ">" + utils.monospace(utils.linkTo(type)) + "</span></li>";
			html += "<li class=" + CLASS_DESCRIPTION + ">" + description + "</li>";
			html += "</li>";

			html += "</ul>"; // close sub-list
		}
		return html;
	}

	// Returns the HTML that inflates the list of arguments for a method of this API
	function inflateArguments(args) {
		var html = "";
		html += "<p><span class=" + CLASS_ARGUMENTS + ">Arguments: </span>";
		if (args.length == 0) {
			html += "None";
		} else {
			html += "<ul>";
			for (var k = 0; k < args.length; k++) {
				html += "<li>" + utils.monospace(args[k].name) + ": " + utils.monospace(utils.linkTo(args[k].type));
				html += "<ul>"; // sub-list everything under args[k].name

				if (args[k].description) {
					html += "<li class=" + CLASS_DESCRIPTION + ">" + args[k].description + "</li>";
				}
				if (args[k].default) {
					html += "<li class=" + CLASS_DEFAULT + ">Default value: " + utils.monospace(args[k].default) + "</li>";
				}

				html += "</ul>"; // close sub-list
				html += "</li>";
			}
			html += "</ul>";
		}
		html += "</p>";
		return html;
	}

	// Returns the HTML that inflates a single method for this API
	function inflateMethod(method) {
		var html = "";
		var name 		= method.name;
		var args 		= method.arguments; // list
		var returnType 	= method.returnType;
		var access 		= method.access;
		var description = method.description;
		html += "<h4 class=" + CLASS_NAME + ">" + utils.monospace(name) + "</h4>";
		html +="<ul>";	// sub-list everything under method.name

		// Inflate arguments
		html += inflateArguments(args);

		// Other properties of the method
		html += "<li><span class=" + CLASS_RETURN_TYPE + ">Returns: </span>" + utils.monospace(utils.linkTo(returnType)) + "</li>";
		html += "<li><span class=" + CLASS_ACCESS + ">Access: </span>" + utils.monospace(access) + "</li>";
		if (method.overrides) {
			html += "<li><span class=" + CLASS_OVERRIDES + ">Overrides: </span>" + utils.monospace(method.overrides) + "</li>";
		}
		html += "<li class=" + CLASS_DESCRIPTION + ">" + description + "</li>";

		html += "</ul>";  // close sub-list
		return html;
	}

	// Returns the HTML that inflates all the method categories of this API
	function inflateMethodCategories(methodCategories) {
		if (methodCategories.length == 0) {
			return HTML_NONE;
		}

		var html = "";
		for (var i = 0; i < methodCategories.length; i++) {
			var category = methodCategories[i].category;
			html += "<li>";
			html += "<h3 class=" + CLASS_HEADING_SECTION + ">" + category + "</h3>";

			// Inflate individual methods
			var methods  = methodCategories[i].methods; // list
			html += "<ul>";
			if (methods.length > 0) {
				for (var j = 0; j < methods.length; j++) {
					html += inflateMethod(methods[j]);
				}
			} else {
				html += HTML_NONE;
			}
			html += "</ul>";

			html += "</li>";
		}
		return html;
	}

	// Returns the HTML that inflates the list of subclasses for this API
	function inflateSubclasses(subclasses) {
		if (subclasses.length == 0) {
			return HTML_NONE;
		}

		var html = "<ul>";
		for (var i = 0; i < subclasses.length; i++) {
			html += "<li>" + utils.monospace(utils.linkTo(subclasses[i].name)) + "</li>";
		}
		html += "</ul>";
		return html;
	}



	//-----------------------------------------------
	// Main procedure
	//-----------------------------------------------

	// Add API HTML content to the main-content div
	$ajaxUtils.sendGetRequest(utils.CONTENTS_FILE, 
		function (contentsResponse) {
			objs = JSON.parse(contentsResponse);

			// Only retrieve the object's JSON if it exists
			if (utils.contains(objs, objName)) {
				$ajaxUtils.sendGetRequest("snippet-api.html", 
					function (snippetResponse) {
						utils.insertHtmlById(utils.ID_MAIN_CONTENT, snippetResponse);

						// Once the HTML snippet has been inserted, inject JSON file into this
						// API page
						var objFile = objName + ".json";
						$ajaxUtils.sendGetRequest(objFile, 
							function(objResponse) {
								var obj = JSON.parse(objResponse);

								// Set title, heading, and desription
								utils.insertHtmlById("heading-obj-name", utils.monospace(obj.name));
								//document.getElementById("heading-obj-name").textContent = obj.name;
								document.getElementById("obj-description").textContent = obj.description;

								// Inflate constants
								utils.insertHtmlById("list-constants", inflateConstants(obj.constants));

								// Inflate instance variables
								utils.insertHtmlById("list-instance-variables", inflateInstanceVariables(obj.instanceVariables));

								// Inflate method categories
								utils.insertHtmlById("list-method-categories", inflateMethodCategories(obj.methodCategories));

								// Inflate subclasses
								utils.insertHtmlById("list-subclasses", inflateSubclasses(obj.subclasses));
							});
					});
			} else {
				// Show error page
				$ajaxUtils.sendGetRequest("snippet-error.html", 
					function (errorResponse) {
						utils.insertHtmlById(utils.ID_MAIN_CONTENT, errorResponse);
						utils.insertHtmlById("heading-error", "Error: " + utils.monospace(objName) + " not found.");
					});
			}
		});
}