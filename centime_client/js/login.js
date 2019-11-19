$(document).ready(() => {

    $("#main-wrapper").hide();
    
    $("#login_button").click(() => {
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/accounts/google/login",
            success: function (data) {
                chrome.windows.create({'url': 'http://127.0.0.1:8000/accounts/google/login', 'type': 'popup'}, function(window) {
                });
                console.log(data.url)
                $("#login_container").hide();
                $('#main-wrapper').show();
                chrome.browserAction.setPopup({ popup:"popup.html" });
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
