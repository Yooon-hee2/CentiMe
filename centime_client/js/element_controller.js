//var totalData = 1000;    // 총 데이터 수
var dataPerPage = 4;    // 한 페이지에 나타낼 데이터 수
var pageCount = 5;        // 한 화면에 나타낼 페이지 수
index = 0;

function paging(totalData, dataPerPage, pageCount, currentPage, container, index){ //container = [날짜, [오차 수치 묶음]]
    //alert(container)
    //alert(container[0].slice(3, container[0].length))
    var totalPage = Math.ceil(totalData/dataPerPage);    // 총 페이지 수
    var pageGroup = Math.ceil(currentPage/pageCount);    // 페이지 그룹
    
    var last = pageGroup * pageCount;    // 화면에 보여질 마지막 페이지 번호
    if(last > totalPage)
        last = totalPage;
    var first = last - (pageCount-1);    // 화면에 보여질 첫번째 페이지 번호
    var next = last+1;
    var prev = first-1;    
    var html = "";
    var cnt = 0;
    
    for (cnt = index; cnt < index+4; cnt++) {
        var slicenum = container[cnt].slice(1, container[0].length).length * (1 / 2);
        var ins = "";

        ins += '<p><div id="size-history" style="height: 60px;">';
        ins += '<span style="font-size: 15px; margin-right: 190px;">' + container[cnt][0] + '</span><span style="color:red; font-size: 15px; margin-right: 12px; float: right; "> 삭제 </span>';
        ins += '<div id="thumbnail" style="float: left; width: 20%;"><img src="./images/img_jeans.png" style="width: 80px; height: 110px;"></div>';
        ins += '<div style="float: left; width: 77%; vertical-align: middle; margin-left: 5px;"><table class="size-table"><thead><tr id = "registered_info">';
        ins += container[cnt].slice(1,slicenum+1) + '</tr></thead><tbody><tr id = "registered_num">' + container[cnt].slice(slicenum+1,container[cnt].length) + '</tr></tbody></table></div></div></p><br/><br/><br/>';
        html += ins;
        
    }
    
    if(prev > 0)
        html += "<a href=# id='prev'><--- prev    </a> ";

    // for(var i=first; i <= last; i++){
    //     html += "<a href='#' id=" + i + ">" + i + "</a> ";
    // }
    
    if(last < totalPage)
        html += "<a href=# id='next'>    next ---></a>";
    //alert(html)
    $("#collapse-content").html(html);    // 페이지 목록 생성
    $("#collapse-content a").css("color", "black");
    $("#collapse-content a#" + currentPage).css({"text-decoration":"none", 
                                       "color":"red", 
                                       "font-weight":"bold"});    // 현재 페이지 표시
                                       
    $("#collapse-content a").click(function(){
        
        var $item = $(this);
        var $id = $item.attr("id");
        var selectedPage = $item.text();
        
        if ($id == "next") {
            selectedPage = next;
            index += 4;
    
        }
        else if ($id == "prev") {
            selectedPage = prev;
            index -= 4;
        }
       
        alert(index)
        paging(totalData, dataPerPage, pageCount, selectedPage, container,index);
    });
                                       
}



$(document).ready(() => {

    var cate_dic = {
        'OUTER': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
        'TOP': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
        'SKIRT': ['waist', 'hip', 'hem', 'length'],
        'PANTS': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
        'OPS': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']
    };

    $("#input-size-menu").click(() => {
        $("#register-container").hide();
        $("#clothes_category_input_container").show();
        $('body').css({
            'background-color': '#fff'
        });
        $("#category_register").click(() => {
            $("#size-form *").remove();
            
            var sel_category = $("input[name='radio']:checked").val();
            
            $("#clothes_category_input_container").hide();
            $("#clothes_size_input_container").show();
            var tmp = Object.keys(cate_dic);
            var sel_list = cate_dic[sel_category];
            for (var i = 0; i < sel_list.length; i++) {
                var info = '<div class="input_group"><input name="'+sel_list[i]+'" type="number" required /><span class="highlight"></span><span class="bar"></span><label class="clothes_size">' + sel_list[i] + '</label></div>';
                $("#size-form").append(info);
            }
            //$("#size-form").append('<div id="btn-box"><button class="submit_button_small">완료</button></div>');
            $("#size-form").append('<strong style="margin-bottom: 20px; font-size: 12px;">어떤 핏으로 입으셨나요 ?</strong>');
            $("#size-form").append('<label class="clothes_fit_container">몸에 딱 맞는 보통핏<input type="radio" checked="checked" name="fit-radio" value="보통핏"><span class="checkmark" ></span></label>');
            $("#size-form").append('<label class="clothes_fit_container">넉넉한 오버핏<input type="radio" name="fit-radio" value="오버핏"><span class="checkmark"></span></label>');
            $("#size-form").append('<div id="btn-box"><button class="submit_button_small">등록하기</button></div>');
            
            var sel_fit = $("input[name='fit-radio']:checked").val();

            $("#size-form").submit(() => {
                if ($("#size-form").get(0).checkValidity()) {
                    $("input[name='radio']").prop("checked", false);
                    $('#clothes_size_input_container').hide().prop('required', false);
                    $('body').css({
                        'background-color': '#fff'
                    });
                    var data = '';
                    $.each( $("#size-form").serializeArray(), function(key, val){
                        data += ',"' + val.name + '":"' + val.value + '"';
                    });
                    data = '{' + data.substr(1) + '}';
                    
                    $.ajax({
                        type: "POST",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/info/personal/",
                        data: JSON.stringify({ sel_category : sel_category, data : data }),
                        dataType: "json",
                        success: function (data) {
                            alert("success");
                            $('#main-wrapper').show();
                        },
                        failure:
                        function (err) {
                            console.log(err);
                        },
                        error: function (request, status, error) {
                            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                        }
                    });alert("수치가 등록됩니다.")

                }   
            });
        });
    });
    // $(".submit_button_small").click(() => {

    //     $("#clothes_category_input_container").hide();
    //     $("#clothes_size_input_container").show();

    // });

    
    $("#register-menu").click(() => {
        $("#main-wrapper").hide();
        $("#register-container").show();
        $('body').css({
            'background-color': '#fff'
        });
    });

    var fit = '보통핏';
    var size = 'S';
    $(document).on('click','#like-menu',function(){
        $("#register-container").hide();
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
            //$(this).attr('src', "./images/img_heart_fill.png");
        });    
    });

    
    $("#recommend_menu").click(() => {
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
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
                    var listval = recommender[key];
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
                //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                alert("정보 등록 후 이용해주세요")
                }
            });

    });
    $("#back_button").click(() => {
        $("#recommend_container").hide();
        $("#main-wrapper").show();
    });
    var togglecount = 0;
    $("#recotoggle").click(() => {
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
        //alert(togglecount)
        if (togglecount == 0) {
            $("input:checkbox[id='recotoggle']").prop("checked", true);
            togglecount++;
            $("#back_button").hide();
            chrome.browserAction.setPopup({ popup: "recommend_window.html" });
        }
        else if (togglecount == 1) {
            $("#recommend_container").hide();
            togglecount = 0;
            $("input:checkbox[id='re_toggle']").prop("checked", false);
            $("input:checkbox[id='recotoggle']").prop("checked", false);
            $("#back_button").show();
            $("#main-wrapper").show();
            chrome.browserAction.setPopup({ popup: "popup.html" });
        }
    });

    $("#re_toggle").click(() => {
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
        //alert(togglecount)
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
                //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                alert("정보 등록 후 이용해주세요")
                }
        });
        togglecount++;
        $("input:checkbox[id='recotoggle']").prop("checked", true);
        chrome.browserAction.setPopup({ popup: "recommend_window.html" });
    });

    $(".tab-slider--nav li").click(function () {
        $("#size-table-list-large *").remove()
        $("#size-table-info-large *").remove()
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
                    var listval_large = recommender_large[key_large];
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
                alert("정보 등록 후 이용해주세요");
            }
        });
    });
       
    $(".collapsible").click(function () {
        var ref_this = $("li.tab-slider--trigger.active")
        var fit_data = ref_this.attr("value");
        if ($("#collapse-content").css("display") == "none") {
            $.ajax({
                type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/all/",
            data: { fit : fit_data},
            dataType: "json",
                success: function (data) {
                    var container = [];
                    
                    var recommend_data = data['reco_dic']; //{'count': [날짜 - 등록된 수치 - 오차 수치],'count': [날짜 - 등록된 수치 - 오차 수치]..}
                                            
                    for (key in recommend_data) {
                        var tp_listcontainer = [];
                        var tp_infocontainer = [];
                        var listdata = recommend_data[key];
                        var date = [listdata[0]];
                        var registered = listdata[1];
                        var errdic = listdata[2];

                        cnt = 0;
                        
                        for (listkey in errdic) { //{waist: , length: , ...}
                            for (sizeinfo in errdic[listkey]) {
                                
                                var tp_list = '<th scope="cols">' + sizeinfo + '</th>';
                                var tp_info = '<td>' + registered[cnt] + '(<strong style="color:red">' + errdic[listkey][sizeinfo] + '</strong>)' + '</td>';
                                tp_listcontainer.push(tp_list);
                                tp_infocontainer.push(tp_info);
                                cnt++;
                            }
                        }
                        var re = tp_listcontainer.concat(tp_infocontainer)
                        //alert(date.concat(re))
                        container.push(date.concat(re));
                        
                    }
                    paging(Object.keys(recommend_data).length, dataPerPage, pageCount, 1, container, index);
                    
                    
            },
            failure:
                function (err) {
                console.log(err);
                },
            error: function (request, status, error) {
                alert("정보 등록 후 이용해주세요");
            }

            });
            $("#collapse-content").show("fast");
        } else {
            $("#collapse-content").hide("fast");
        }
    });
    $("#tab1_trend").click(function(){
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/trend/",
            data: { fit: '보통핏'},
            dataType: "json",
            success: function (data) {
                var recommender = data['reco'];
                for (key in recommender) {
                    var listval = recommender[key]
                    for (list_key in listval) {
                        $("#reco_size").html('추천 사이즈 : <strong>'+key+'</strong>');
                        var tmp_list = '<th scope="cols">' + list_key + '</th>';
                        var tmp_info = '<td>' + listval[list_key].toFixed(2) + '</td>';
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
                //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                alert("정보 등록 후 이용해주세요")
                }
        });

    });
    $("#tab2_trend").click(function(){
        $("#size-table-list-large *").remove();
        $("#size-table-info-large *").remove();
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/trend/",
            data: { fit: '오버핏'},
            dataType: "json",
            success: function (data) {
                var recommender_large = data['reco'];
                for (key_large in recommender_large) {
                    var listval_large = recommender_large[key_large]
                    for (list_key_large in listval_large) {
                        $("#reco_size_large").html('추천 사이즈 : <strong>'+key_large+'</strong>');
                        var tmp_list_large = '<th scope="cols">' + list_key_large + '</th>';
                        var tmp_info_large = '<td>' + listval_large[list_key_large].toFixed(2) + '</td>';
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
                //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                alert("정보 등록 후 이용해주세요")
                }
        });

    });
      

    

    $(".tab-slider--body").hide();
    $(".tab-slider--body:first").show();
    // $("#main-wrapper").hide();
    $("#register-container").hide();
    $("#like_container").hide();
    $("#size_container").hide();
    $("#recommend_container").hide();
    $("#clothes_category_input_container").hide();
    $("#clothes_size_input_container").hide();
    $("#clothes_fit_input_container").hide();

});
