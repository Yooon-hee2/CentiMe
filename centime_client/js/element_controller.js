$(document).ready(() => {
    var cate_dic = {
        'OUTER': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
        'TOP': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
        'SKIRT': ['waist', 'hip', 'hem', 'length'],
        'PANTS': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
        'OPS': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']
    };
    
    $("#login_button").click(() => {
        $("#login_container").hide();
        //$("#body_size_input_container").show();
        $('#main-wrapper').show();
        alert("Welcome");
    });

    $("#input_size_menu").click(() => {
        $("#main-wrapper").hide();
        $("#clothes_category_input_container").show();
        $('body').css({
            'background-color': '#fff'
        });
        $("#category_register").click(() => {
            var sel_category = $("input[name='radio']:checked").val();
            $("#clothes_category_input_container").hide();
            $("#clothes_size_input_container").show();
            var tmp = Object.keys(cate_dic);
            var sel_list = cate_dic[sel_category];
            for (var i = 0; i < sel_list.length; i++) {
                var info = '<div class="input_group"><input name="'+sel_list[i]+'" type="number" required /><span class="highlight"></span><span class="bar"></span><label class="clothes_size">' + sel_list[i] + '</label></div>';
                $("#size-form").append(info);
            }
            $("#size-form").append('<div id="btn-box"><button class="submit_button_small">완료</button></div>');
        
            $("#size-form").submit((event) => {
                event.preventDefault();
                if ($("#size-form").get(0).checkValidity()) {
                    $('#clothes_size_input_container').hide().prop('required', false);
                    $('body').css({
                        'background-color': '#fff'
                    });
                    var data = '';
                    $.each( $("#size-form").serializeArray(), function(key, val){
                        data += ',"' + val.name + '":"' + val.value + '"';
                    });
                    alert(data)
                    data = '{'+ data.substr(1) +'}';
                    $.ajax({
                        type: "POST",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/info/personal/",
                        data: JSON.stringify({ sel_category : sel_category, data : data }),
                        dataType: "json",
                        success: function (data) {
                            alert("success")
                        },
                        failure:
                        function (err) {
                            console.log(err);
                        },
                        error: function (request, status, error) {
                            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                        }
                    });
                    $('#main-wrapper').show();
                
                }   
            });
        });
    });
    // $(".submit_button_small").click(() => {

    //     $("#clothes_category_input_container").hide();
    //     $("#clothes_size_input_container").show();

    // });

    






    var fit = '보통핏';
    var size = 'S';
    $(document).on('click','#like_menu',function(){
        
        
        // chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
        //     var url = tabs[0].url;
        //     alert(url)
        // });
        
        $("#main-wrapper").hide();
        $("#like_container").show();
        $('body').css({
            'background-color': 'rgb(255, 145, 123)'
        }); 
        var url = "https://m.ba-on.com/product/list.html?cate_no=35";
        
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/info/",
            data: JSON.stringify({ url: url }),
            dataType: "json",
            success: function (data) {
                var re_data = data['re_dic'];
                var button = document.getElementById("fit1");
                button.addEventListener("click", function () {
                    fit = $("#fit1").text();
                    $("#like_container").hide();
                    for (var key in re_data) {
                        var tmp = '<button class="fit_button" id="size_sel">' + key + '</button>';
                        $("#size_container").append(tmp);
                    }
                    re_data = [];
                    this.removeEventListener("click", arguments.callee);
                }, false);
                button.removeEventListener("click", function () { });
                var button2 = document.getElementById("fit2");
                button2.addEventListener("click", function () {
                    fit = $("#fit2").text();
                    $("#like_container").hide();
                    for (var key in re_data) {
                        var tmp = '<button class="fit_button" id="size_sel">' + key + '</button>';
                        $("#size_container").append(tmp);  
                    }
                    re_data = [];
                    this.removeEventListener("click",arguments.callee);
                }, false);
                button2.removeEventListener("click", function () { });
                $("#size_container").show();
            },
                failure:
                function (err) {
                    alert("정보를 찾을 수 없습니다.")
                },
                error:function(request,status,error){
                    alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                 }
       
        }); 
        var checked = false;
        $("#size_container").click(() => {
            $(document).on("click","#size_sel",function(){
                size = $(this).text(); 
            if(checked == false){
                checked = true
            
                $.ajax({
                type: "POST",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/info/store/",
                data: JSON.stringify({ fit: fit, size: size}),
                dataType: "json",
                success: function (data) {
                    size = ''
                    $("#like_container").hide();
                    alert("success");
                    $("#main-wrapper").show();
                    $("#size_container *").remove();
                },
                failure:
                function (err) {
                        console.log(err);
                    },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                }
            });
            }     
        });     
            $('body').css({
                'background-color': '#fff'
            });
            $(this).attr('src', "./images/img_heart_fill.png");
        });    
    });

    


    
    $(".collapsible").click(function() {
        $('#recent_details_container').show();
    });
    
    $("#recommend_menu").click(() => {
        $("#main-wrapper").hide();
        $("#recommend_container").show();
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
                        $("#reco_size").html('추천 사이즈 : <strong>'+key+'</strong>');
                        var tmp_list = '<th scope="cols">' + list_key + '</th>';
                        var tmp_info = '<td>' + listval[list_key] + '</td>';
                        $("#size-table-list").append(tmp_list);
                        $("#size-table-info").append(tmp_info);
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
    $("#back_button").click(() => {
        $("#recommend_container").hide();
        $("#main-wrapper").show();
    });
    $("#recotoggle").click(() => {
        $("input:checkbox[id='re_toggle']").prop("checked", true);
        $("#back_button").hide();
        chrome.browserAction.setPopup({ popup:"recommend_window.html" });
    });

    $("#toggleclick").click(() => {
        $("#main-wrapper").hide();
        $("#back_button").hide();
        $("#recommend_container").show();
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
                        $("#reco_size").html('추천 사이즈 : <strong>'+key+'</strong>');
                        var tmp_list = '<th scope="cols">' + list_key + '</th>';
                        var tmp_info = '<td>' + listval[list_key] + '</td>';
                        $("#size-table-list").append(tmp_list);
                        $("#size-table-info").append(tmp_info);
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
        $("input:checkbox[id='recotoggle']").prop("checked", true);
        chrome.browserAction.setPopup({ popup:"recommend_window.html" });
    });
    
    
        




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
                        $("#reco_size_large").html('추천 사이즈 : <strong>'+key_large+'</strong>');
                        var tmp_list_large = '<th scope="cols">' + list_key_large + '</th>';
                        var tmp_info_large = '<td>' + listval_large[list_key_large] + '</td>';
                        $("#size-table-list-large").append(tmp_list_large);
                        $("#size-table-info-large").append(tmp_info_large);
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
    $("#main-wrapper").hide();
    $("#like_container").hide();
    $("#size_container").hide();
    $("#recommend_container").hide();
    $("#clothes_category_input_container").hide();
    $("#clothes_size_input_container").hide();

});
