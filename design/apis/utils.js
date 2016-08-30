/*
 * Description: This creates an object containing helper functions and other
 * utilities common to all HTML pages in this app.
 */

(function (global) {

// Set up a namespace for utils
var utils = {};

// Constants
utils.ID_MAIN_CONTENT 		= "main-content";
utils.ID_TABLE_OF_CONTENTS 	= "table-of-contents";
utils.CONTENTS_FILE 		= "objects.json";

// Returns true if the item is in the list, false if not
utils.contains = function (list, item) {
	for (var i = 0; i < list.length; i++) {
		if (list[i] === item) {
			return true;
		}
	}
	return false;
}

// Inserts the given html string into the element with the given ID
utils.insertHtmlById = function (id, html) {
	document.getElementById(id).innerHTML = html;
};

// Adds the given html string to the existing content in the element with the given
// ID
utils.addHtmlById = function (id, html) {
	document.getElementById(id).innerHTML += html;
};

// Returns the HTML that generates a link to the given object's API page
// TODO: Should not make a link for non-existing types like int, void, and boolean
utils.linkTo = function (objectName) {
	return "<a href=# onclick='loadAPI(\"" + objectName + "\");'>" + objectName + "</a>";
};

// Returns the HTML that converts the given text to code (monospace)
utils.monospace = function (text) {
	return "<code>" + text + "</code>";
};

// Attach these utils to the global scope
global.utils = utils;

})(window);