var website = document.getElementById("websitetocheck").value;
var result
var match
console.log(website)
if (match = website.match(/^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n\?\=]+)/im)) {
    result = match[1]
    if (match = result.match(/^[^\.]+\.(.+\..+)$/)) {
        result = match[1]
    }
}

var xhttp = new XMLHttpRequest();
var url = "https://haveibeenpwned.com/api/v2/breaches?domain=";
var domain = result

var checkUserURL = url + domain;
xhttp.onreadystatechange = function () {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
        writeData(xhttp.responseText);
    } else if (xhttp.readyState == 4 && xhttp.status == 404) {
        document.getElementById("breachInfo").innerHTML = "";
    }
};
xhttp.open("GET", checkUserURL, true);
xhttp.send();
console.log(status = xhttp.status)

function writeData(response) {
    var arr = JSON.parse(response);
    var i;
    var website = document.getElementById("websitetocheck").value;
    console.log(website)
    console.log(arr)
    if (arr.length == 0) {
        document.getElementById("breachInfo").innerHTML = ""
    } else {
        var out = "<h4><span class=\"attention\">Unfortunately, it looks like \"" + website + "\" has been breached. </span>Please see the details below:</h4>";
        for (i = 0; i < arr.length; i++) {
            out += "<div class=\"form-group row\">" +
                "<strong class=\"col-sm-2 col-form-label\">Domain of Breach:&nbsp;</strong>" +
                "<div class=\"col-sm-10\">" +
                arr[i].Name +
                "&nbsp;(<a href=\"http://" + arr[i].Domain + "\" target=\"_blank\">" +
                "http://" + arr[i].Domain + "</a>):&nbsp;" +
                "</div>" +
                "</div>" +
                "<div class=\"form-group row\">" +
                "<div class=\"col-sm-2\"></div> " +
                "<div class=\"col-sm-10\">" +
                "<div class=\"breachDesc\">" +
                arr[i].Description +
                "</div>" +
                "</div>" +
                "</div>" +
                "<div class=\"form-group row\">" +
                "<strong class=\"col-sm-2\">Breached Items:&nbsp;</strong>" +
                "<div class=\"col-sm-10\">" +
                arr[i].DataClasses +
                "</div>" +
                "</div>" +
                "<div class=\"form-group row\">" +
                "<strong class=\"col-sm-2\">Breach Date:&nbsp;</strong> " +
                "<div class=\"col-sm-10\">" +
                arr[i].BreachDate +
                "</div>" +
                "</div>";
        }
        out += "</div>";
        document.getElementById("breachInfo").innerHTML = out;
    }
}

function reloadMe() {
    window.location = window.location.pathname;
}