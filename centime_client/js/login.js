$(document).ready(() => {

    $.ajax({
        type: "GET",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/checklogin",
        success: function (data) {
            if(data.message == "already logined"){
                alert("already logined");
                window.location.href = "popup.html";
                chrome.browserAction.setPopup({ popup:"popup.html" });
            }
            else if(data.message == "anonymous"){
                alert("login please");
                chrome.browserAction.setPopup({ popup:"login.html" });
            }   
        }
    });

    $("#login_button").click(() => {
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/accounts/google/login",
            success: function (data) {
                chrome.windows.create({ 'url': 'http://127.0.0.1:8000/accounts/google/login', 'type' : 'popup' }, function (window) {});
                window.close();
            },
            failure:
                function (err) {
                    console.log(err);
                },
            error: function (request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            }
        });
    });
});

//로그인 전체부분