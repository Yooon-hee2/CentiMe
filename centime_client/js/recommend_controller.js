//var totalData = 1000;    // 총 데이터 수
var dataPerPage = 4;      // 한 페이지에 나타낼 데이터 수
var pageCount = 5;        // 한 화면에 나타낼 페이지 수
index = 0;

function paging(totalData, dataPerPage, pageCount, currentPage, container, index){ //container = [날짜, [오차 수치 묶음]]
    
    //alert(container[0].slice(3, container[0].length))
    var totalPage = Math.ceil(totalData/dataPerPage);    // 총 페이지 수
    
    // var last = pageCount;    // 화면에 보여질 마지막 페이지 번호
    // if (last > totalPage) {
    //     last = totalPage;
    // }
    var next = currentPage+1;
    var prev = currentPage-1;    
    var html = "";
    var cnt = 0;
    
    for (cnt = index; cnt < index + 4; cnt++) {
        var slicenum = container[cnt].slice(2, container[0].length+1).length * (1 / 2);
        var ins = "";
        src_temp = container[cnt][1];
        if (src_temp == 'OPS' || src_temp == 'OUTER' || src_temp == 'PANTS' || src_temp == 'TOP' || src_temp == 'SKIRT') {
            src_temp = "./images/img_" + container[cnt][1] + ".png";
        }
        src_temp = container[cnt][1];
        if (src_temp == 'OPS' || src_temp == 'OUTER' || src_temp == 'PANTS' || src_temp == 'TOP' || src_temp == 'SKIRT') {
            src_temp = "./images/img_" + container[cnt][1] + ".png";
        }

        ins += '<p><div id="size-history" style="height: 60px;">';
        ins += '<span style="font-size: 15px; margin-right: 190px;">' + container[cnt][0] + '</span><span style="color:red; font-size: 15px; margin-right: 12px; float: right; "> 삭제 </span>';
        ins += '<div id="thumbnail" style="float: left; width: 20%; margin-left:5px"><img src="'+ src_temp+'" style="height: 125px; width: 100px; border-radius: 15px; border: 0px;"></div>';        ins += '<div style="float: left; width: 77%; vertical-align: middle; margin-left: 5px;"><table class="size-table"><thead><tr id = "registered_info">';
        ins += '<div style="float: left; width: 77%; vertical-align: middle; margin-left: 5px;"><table class="size-table"><thead><tr id = "registered_info">';
        ins += container[cnt].slice(2,2+slicenum) + '</tr></thead><tbody><tr id = "registered_num">' + container[cnt].slice(slicenum+2,container[cnt].length) + '</tr></tbody></table></div></div></p><br/><br/><br/>';
        html += ins;
    }
    
    if (prev > 0) {
        html += "<a href=# id='prev'><--- prev    </a> ";
    }
    
    
    if (next <= totalPage) {
        html += "<a href=# id='next'>    next ---></a>";
    }
    
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
        
        paging(totalData, dataPerPage, pageCount, selectedPage, container,index);
    });
                                       
}

$(document).ready(() => {
    $("#size-table-list *").remove();
    $("#size-table-info *").remove();
    var currentUrl = '';
    var categoryUrl = '';

    var urlArray = new Array();
    chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
            currentUrl = tabs[0].url;
    });
    chrome.history.search({ text: '', maxResults: 10 }, function (data) {
        var i, j = 0;
        data.forEach(function (page) {
            urlArray.push(page.url)
        });
        for (i = 1; i < urlArray.length; i++) {
            if (currentUrl.replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]
                == urlArray[i].replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]) {
                if (currentUrl != urlArray[i]) {
                    categoryUrl = urlArray[i];
                    break;
                }
            }
        }
            
        $.ajax({
            type: "GET",
            ContentType: 'application/json',
            url: "http://127.0.0.1:8000/recommend/recent/",
            data: { fit: '보통핏', url_send :encodeURIComponent(currentUrl), category_url:encodeURIComponent(categoryUrl)},
            dataType: "json",
            success: function (data) {
                var cate_ui = data['category'];
                var recommender = data['reco'];
                $("#cate_ui").attr("src","./images/img_"+cate_ui+".png");
    
                for (key in recommender) {
                    var listval = recommender[key];
                    for (list_key in listval) {
                        $("#reco_size").html('추천 사이즈 : <strong>' + key + '</strong>');
                        var tmp_list = '<th scope="cols">' + list_key + '</th>';
                        var tmp_info = '<td>' + listval[list_key] + '</td>';
                        $("#size-table-list").append(tmp_list);
                        $("#size-table-info").append(tmp_info);
                    }
                }
            },
            beforeSend: function () {
                $("#cate_ui").attr("src", "https://berserkon.com/images/loading-transparent-animated-gif.gif");
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




    $("#pops").click(() => {
        $("input:checkbox[id='pop_toggle']").prop("checked", false);
        $("#back_button").show();
        alert("추천모드 해제");
        window.close();
        chrome.browserAction.setPopup({ popup: "popup.html" });
    });

    $(".tab-slider--nav li").click(function () {
        $("#size-table-list-large *").remove()
        $("#size-table-info-large *").remove()
        $(".tab-slider--body").hide();
        var activeTab = $(this).attr("rel");
        $("#" + activeTab).fadeIn();
        if ($(this).attr("rel") == "tab2") {
            $('.tab-slider--tabs').addClass('slide');
        } else {
            $('.tab-slider--tabs').removeClass('slide');
        }
        $(".tab-slider--nav li").removeClass("active");
        $(this).addClass("active");
        
        var currentUrl = '';
        var categoryUrl = '';
        var urlArray = new Array();
        chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true }, function (tabs) {
            currentUrl = tabs[0].url;
        });
        chrome.history.search({ text: '', maxResults: 10 }, function (data) {
            var i, j = 0;
            data.forEach(function (page) {
                urlArray.push(page.url)
            });
            for (j = 0; j < urlArray.length; j++) {
                console.log(urlArray[j]);
            } //for check, will be erased
            for (i = 1; i < urlArray.length; i++) {
                if (currentUrl.replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]
                    == urlArray[i].replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]) {
                    if (currentUrl != urlArray[i]) {
                        categoryUrl = urlArray[i];
                        break;
                    }
                }
            }
            $.ajax({
                type: "GET",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/recommend/recent/",
                data: { fit: '오버핏', url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var recommender_large = data['reco'];

                    for (key_large in recommender_large) {
                        var listval_large = recommender_large[key_large];
                        for (list_key_large in listval_large) {
                            $("#reco_size_large").html('추천 사이즈 : <strong>' + key_large + '</strong>');
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
    });
    $(".collapsible").click(function () {
        var ref_this = $("li.tab-slider--trigger.active")
        var fit_data = ref_this.attr("value");
        if ($("#collapse-content").css("display") == "none") {
            var currentUrl = '';
            var categoryUrl = '';

            var urlArray = new Array();
            chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
                currentUrl = tabs[0].url;
            });
            chrome.history.search({ text: '', maxResults: 10 }, function (data) {
                var i, j = 0;
                data.forEach(function (page) {
                    urlArray.push(page.url)
                });
                
                for (i = 1; i < urlArray.length; i++) {
                    if (currentUrl.replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]
                        == urlArray[i].replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]) {
                        if (currentUrl != urlArray[i]) {
                            categoryUrl = urlArray[i];
                            break;
                        }
                    }
                }

                $.ajax({
                    type: "GET",
                    ContentType: 'application/json',
                    url: "http://127.0.0.1:8000/recommend/all/",
                    data: { fit: fit_data, url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                    dataType: "json",
                    success: function (data) {
                        var container = [];
                    
                        var recommend_data = data['reco_dic']; //{'count': [날짜 - 등록된 수치 - 오차 수치-thumbnail],'count': [날짜 - 등록된 수치 - 오차 수치]..}
                                            
                        for (key in recommend_data) {
                            var tp_listcontainer = [];
                            var tp_infocontainer = [];
                            var listdata = recommend_data[key];
                            var date = [listdata[0]];
                            var thumb = [listdata[3]];
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
                            var thumb = thumb.concat(re)
                            container.push(date.concat(thumb));
                        
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
            });
            $("#collapse-content").show("fast");
        } else {
            $("#collapse-content").hide("fast");
        }
    });

    $("#tab1_trend").click(function(){
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
        var currentUrl = '';
        var categoryUrl = '';
        var urlArray = new Array();
        chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
            currentUrl = tabs[0].url;
        });
        chrome.history.search({ text: '', maxResults: 10 }, function (data) {
            var i, j = 0;
            data.forEach(function (page) {
                urlArray.push(page.url)
            });
            for (j = 0; j < urlArray.length; j++) {
                console.log(urlArray[j]);
            } //for check, will be erased
            for (i = 1; i < urlArray.length; i++) {
                if (currentUrl.replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]
                    == urlArray[i].replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]) {
                    if (currentUrl != urlArray[i]) {
                        categoryUrl = urlArray[i];
                        break;
                    }
                }
            }
            $.ajax({
                type: "GET",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/recommend/trend/",
                data: { fit: '보통핏',url_send :encodeURIComponent(currentUrl), category_url:encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var recommender = data['reco'];
                    for (key in recommender) {
                        var listval = recommender[key]
                        for (list_key in listval) {
                            $("#reco_size").html('추천 사이즈 : <strong>' + key + '</strong>');
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

    });
    $("#tab2_trend").click(function(){
        $("#size-table-list-large *").remove();
        $("#size-table-info-large *").remove();
        var currentUrl = '';
        var categoryUrl = '';
        var urlArray = new Array();
        chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
            currentUrl = tabs[0].url;
        });
        chrome.history.search({ text: '', maxResults: 10 }, function (data) {
            var i, j = 0;
            data.forEach(function (page) {
                urlArray.push(page.url)
            });
            for (j = 0; j < urlArray.length; j++) {
                console.log(urlArray[j]);
            } //for check, will be erased
            for (i = 1; i < urlArray.length; i++) {
                if (currentUrl.replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]
                    == urlArray[i].replace('http://', '').replace('https://', '').replace('www.', '').split(/[/?#]/)[0]) {
                    if (currentUrl != urlArray[i]) {
                        categoryUrl = urlArray[i];
                        break;
                    }
                }
            }
            $.ajax({
                type: "GET",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/recommend/trend/",
                data: { fit: '오버핏', url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var recommender_large = data['reco'];
                    for (key_large in recommender_large) {
                        var listval_large = recommender_large[key_large]
                        for (list_key_large in listval_large) {
                            $("#reco_size_large").html('추천 사이즈 : <strong>' + key_large + '</strong>');
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
    });
      

    

    

    $(".tab-slider--body").hide();
    $(".tab-slider--body:first").show();
})

