$(document).ready(() => {

    $.ajax({
        type: "GET",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/accounts/google/login",
        success: function (data) {
            if(data.message == "ok"){
                window.location.href = "popup.html";
                alert("already logined");
                chrome.browserAction.setPopup({ popup:"popup.html" });
            }
            else{
                alert("login please");
                // window.location.href = "login.html";
                chrome.browserAction.setPopup({ popup:"login.html" });
            }
        },
        failure:
            function (err) {
                console.log(err);
            },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    });
    $("#login_button").click(() => {
        chrome.windows.create({ 'url': 'http://127.0.0.1:8000/accounts/google/login', 'type' : 'popup' }, function (window) {});
        window.close();
    });

});