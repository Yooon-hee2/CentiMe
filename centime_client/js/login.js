$(document).ready(() => {

    var xhr = new XMLHttpRequest();
    $.ajax({
        type: "GET",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/accounts/google/login",
        xhr: function() {
            return xhr;
        },
        success: function (data) {
            if(xhr.responseURL == "http://127.0.0.1:8000/done/"){
                alert("already logined");
                window.location.href = "popup.html";
                chrome.browserAction.setPopup({ popup:"popup.html" });
            }
            else{
                alert("login please");
                window.location.href = "login.html";
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

//로그인 전체부분