/*
 * Description: This is a set of AJAX utilities taken from Coursera's JHU Ruby On
 * Rails Course 4, Lecture 58. It supports HTTP GET requests that retrieve JSON
 * data.
 */

(function (global) {

// Set up a namespace for our utility
var ajaxUtils = {};


// Returns an HTTP request object
function getRequestObject() {
  if (window.XMLHttpRequest) {
    return (new XMLHttpRequest());
  } 
  else if (window.ActiveXObject) {
    // For very old IE browsers (optional)
    return (new ActiveXObject("Microsoft.XMLHTTP"));
  } 
  else {
    global.alert("Ajax is not supported!");
    return(null); 
  }
}


// Makes an Ajax GET request to 'requestUrl', and passes the response (as a String)
// to the 'responseHandler' function
ajaxUtils.sendGetRequest = 
  function(requestUrl, responseHandler) {
    var request = getRequestObject();
    request.onreadystatechange = 
      function() { 
        handleResponse(request, responseHandler); 
      };
    request.open("GET", requestUrl, true);
    request.overrideMimeType("application/json");
    request.send(null);
  };


// Only calls user provided 'responseHandler' function if response succeeded
// (i.e. not an error)
function handleResponse(request, responseHandler) {
  if ((request.readyState == 4) &&
     (request.status == 200)) {
    responseHandler(request.responseText);
  }
}


// Expose utility to the global object
global.$ajaxUtils = ajaxUtils;


})(window);