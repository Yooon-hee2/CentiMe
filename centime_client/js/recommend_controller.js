$(document).ready(() => {
    $.ajax({
        type: "GET",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/recommend/recent/",
        data: { fit: '보통핏'},
        dataType: "json",
        success: function (data) {
            var recommender = data['reco'];
            console.log(recommender)
            for (key in recommender) {
                var listval = recommender[key]
                for (list_key in listval) {
                    $("#active-size").html('추천 사이즈 : <strong>'+key+'</strong>');
                    var tmp_list = '<th scope="cols">' + list_key + '</th>';
                    var tmp_info = '<td>' + listval[list_key] + '</td>';
                    $("#active-size-list").append(tmp_list);
                    $("#active-size-info").append(tmp_info);
                }
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

    $("#pops").click(() => {
        $("input:checkbox[id='pop_toggle']").prop("checked", false);
        $("#back_button").show();
        alert("추천모드 해제");
        window.close();
        chrome.browserAction.setPopup({ popup: "popup.html" });
    });

    $(".collapsible").click(function() {
        if($("#collapse-content").css("display") == "none"){
            $("#collapse-content").show("fast");
        } else {
            $("#collapse-content").hide("fast");
        }
    });

    // $("#recent_details_container").hide();
    // $('body').css({
    //     'background-color': '#fff'
    // });
    // $(".tab-slider--body").hide();
    // $(".tab-slider--body:first").show();

    $(".tab-slider--nav li").click(function() {
        $(".tab-slider--body").hide();
        var activeTab = $(this).attr("rel");
        $("#"+activeTab).fadeIn();
          if($(this).attr("rel") == "tab2"){
              $('.tab-slider--tabs').addClass('slide');
          }else{
              $('.tab-slider--tabs').removeClass('slide');
          }
        $(".tab-slider--nav li").removeClass("active");
        $(this).addClass("active");
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/recent/",
            data: { fit: '오버핏'},
            dataType: "json",
            success: function (data) {
                var recommender_large = data['reco'];
                for (key_large in recommender_large) {
                    var listval_large = recommender_large[key_large]
                    for (list_key_large in listval_large) {
                        $("#active-size-large").html('추천 사이즈 : <strong>'+key_large+'</strong>');
                        var tmp_list_large = '<th scope="cols">' + list_key_large + '</th>';
                        var tmp_info_large = '<td>' + listval_large[list_key_large] + '</td>';
                        $("#active-list-large").append(tmp_list_large);
                        $("#active-info-large").append(tmp_info_large);
                    }
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
      });
      

    

    $(".tab-slider--body").hide();
    $(".tab-slider--body:first").show();



});

