var cate_dic = {
    'OUTER': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
    'TOP': ['bust', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'length'],
    'SKIRT': ['waist', 'hip', 'hem', 'length'],
    'PANTS': ['waist', 'hip', 'thigh', 'hem', 'crotch_rise', 'length'],
    'OPS': ['waist', 'shoulder', 'armhole', 'sleeve', 'sleevewidth', 'hip', 'length']
};


//var totalData = 1000;    // 총 데이터 수
var dataPerPage = 4;      // 한 페이지에 나타낼 데이터 수
var pageCount = 5;        // 한 화면에 나타낼 페이지 수
index = 0;

function paging(totalData, dataPerPage, pageCount, currentPage, container, index) { //container = [날짜, [오차 수치 묶음]]
    //alert(container[0].slice(3, container[0].length))
    var totalPage = Math.ceil(totalData / dataPerPage);    // 총 페이지 수
    
    var next = currentPage + 1;
    var prev = currentPage - 1;
    var html = "";
    var cnt = 0;
    for (cnt = index; cnt < index + 4; cnt++) {
        var slicenum = container[cnt].slice(2, container[cnt].length + 1).length * (1 / 2);
        var ins = "";
        src_temp = container[cnt][1];
        if (src_temp == 'OPS' || src_temp == 'OUTER' || src_temp == 'PANTS' || src_temp == 'TOP' || src_temp == 'SKIRT') {
            src_temp = "./images/img_" + container[cnt][1] + ".png";
        }
        src_temp = container[cnt][1];
        if (src_temp == 'OPS' || src_temp == 'OUTER' || src_temp == 'PANTS' || src_temp == 'TOP' || src_temp == 'SKIRT') {
            src_temp = "./images/img_" + container[cnt][1] + ".png";
        }

        ins += '<p><div id="size-history-'+cnt+'" style="height: 60px;">';
        ins += '<span style="font-size: 15px; margin-right: 190px;">' + container[cnt][0] + '</span><span id="del" style="color:red; font-size: 15px; margin-right: 12px; float: right; "> 삭제 </span>';
        ins += '<div id="thumbnail" style="float: left; width: 20%; margin-left:5px"><img src="'+ src_temp+'" style="height: 125px; width: 100px; border-radius: 15px; border: 0px;"></div>';        ins += '<div style="float: left; width: 77%; vertical-align: middle; margin-left: 5px;"><table class="size-table"><thead><tr id = "registered_info">';
        ins += container[cnt].slice(2, 2 + slicenum) + '</tr></thead><tbody><tr id = "registered_num">' + container[cnt].slice(slicenum + 2, container[cnt].length) + '</tr></tbody></table></div></div></p><br/><br/><br/>';
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
    $("#collapse-content a#" + currentPage).css({
        "text-decoration": "none",
        "color": "red",
        "font-weight": "bold"
    });    // 현재 페이지 표시

    $("#collapse-content a").click(function () {

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
function add_register(currentUrl, categoryUrl) {
    alert("정보를 찾을 수 없습니다. 수치를 입력해주세요 :)")
    $("#size-form *").remove();
    $.ajax({
        type: "GET",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/info/more",
        data: { url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
        dataType: "json",
        success: function (data) {
            var sel_category = data['cate'];
            $("#like_container").hide();
            //alert(sel_category)
            $("#clothes_size_input_container").show();
            $('body').css({
                'background-color': '#fff'
            });
            var tmp = Object.keys(cate_dic);
            var sel_list = cate_dic[sel_category];
            for (var i = 0; i < sel_list.length; i++) {
                var info = '<div class="input_group"><input name="' + sel_list[i] + '" type="number" required /><span class="highlight"></span><span class="bar"></span><label class="clothes_size">' + sel_list[i] + '</label></div>';
                $("#size-form").append(info);
            }
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
                    $.each($("#size-form").serializeArray(), function (key, val) {
                        data += ',"' + val.name + '":"' + val.value + '"';
                    });
                    data = '{' + data.substr(1) + '}';

                    $.ajax({
                        type: "POST",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/info/personal/",
                        data: JSON.stringify({ sel_category: sel_category, data: data }),
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
                    }); alert("수치가 등록됩니다.")

                }
            });
        },
    failure:
        function (err) {
            console.log(err);
        },
        error: function (request, status, error) {
            alert("수치 등록이 실패했습니다. 다음에 다시 이용해주세요!");
        }
    });
}


$(document).ready(() => {
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
                var info = '<div class="input_group"><input name="' + sel_list[i] + '" type="number" required /><span class="highlight"></span><span class="bar"></span><label class="clothes_size">' + sel_list[i] + '</label></div>';
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
                    $.each($("#size-form").serializeArray(), function (key, val) {
                        data += ',"' + val.name + '":"' + val.value + '"';
                    });
                    data = '{' + data.substr(1) + '}';

                    $.ajax({
                        type: "POST",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/info/personal/",
                        data: JSON.stringify({ sel_category: sel_category, data: data }),
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
                    }); alert("수치가 등록됩니다.")

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
    $(document).on('click', '#like-menu', function () {
        var currentUrl = '';
        var categoryUrl = '';
        $("#register-container").hide();
        $("#like_container").show();
        $('body').css({
            'background-color': 'rgb(255, 145, 123)'
        });

        var urlArray = new Array();
        chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true }, function (tabs) {
            currentUrl = tabs[0].url;
        });
        chrome.history.search({ text: '', maxResults: 20 }, function (data) {
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
            //   alert(currentUrl); //current url for test
            //   alert(categoryUrl); //category url for test

            $.ajax({
                type: "GET",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/info/",
                data: { url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var re_data = data['re_dic'];
                    if (re_data == '') {
                        add_register(currentUrl, categoryUrl);
                    }
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
                        this.removeEventListener("click", arguments.callee);
                    }, false);
                    button2.removeEventListener("click", function () { });
                    $("#size_container").show();
                },
                beforeSend: function () {
                    $("#loading").show();
                },
                complete: function () {
                    $("#loading").hide();
                },
                failure: function (err) {
                    add_register(currentUrl, categoryUrl);
                    },
                error: function (request, status, error) {
                    add_register(currentUrl, categoryUrl);
                    //alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                    //alert("잘못된 url 정보가 입력되었습니다.")
                }
                    
            });
        });
        var checked = false;
        $("#size_container").click(() => {
            $(document).on("click", "#size_sel", function () {
                size = $(this).text();
                if (checked == false) {
                    checked = true
                    $.ajax({
                        type: "POST",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/info/store/",
                        data: JSON.stringify({ fit: fit, size: size, url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) }),
                        dataType: "json",
                        success: function (data) {
                            size = ''
                            $("#like_container").hide();
                            alert("success");
                            $("#main-wrapper").show();
                            $("#size_container *").remove();
                        },
                        beforeSend: function () {
                            $("#loading").show();
                        },
                        complete: function () {
                            $("#loading").hide();
                        },
                        failure:
                            function (err) {
                                console.log(err);
                            },
                        error: function (request, status, error) {
                            alert("저장에 실패했습니다! 다음에 다시 시도해주세요!");
                        }
                    });
                }
            });
            $('body').css({
                'background-color': '#fff'
            });
        });
    });



    $("#recommend_menu").click(() => {
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
        $("#main-wrapper").hide();
        $("#recommend_container").show();
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
            //alert(categoryUrl)
            $.ajax({
                type: "GET",
                ContentType: 'application/json',
                url: "http://127.0.0.1:8000/recommend/recent/",
                data: { fit: '보통핏', url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var cate_ui = data['category'];
                    var recommender = data['reco'];
                    $("#cate_ui").attr("src", "./images/img_" + cate_ui + ".png");
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
                    //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    alert("정보 등록 후 이용해주세요");
                }
            });
        });

    });
    $("#back_button").click(() => {
        $("#recommend_container").hide();
        $("#main-wrapper").show();
    });
    var togglecount = 0;
    $("#recotoggle").click(() => {
        //$("#back_button").hide();
        // $("#size-table-list *").remove();
        // $("#size-table-info *").remove();
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
        var currentUrl = '';
        var categoryUrl = '';
        var urlArray = new Array();
        chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true }, function (tabs) {
            currentUrl = tabs[0].url;
        });
        chrome.history.search({ text: '', maxResults: 20 }, function (data) {
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
                data: { fit: '보통핏', url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                dataType: "json",
                success: function (data) {
                    var cate_ui = data['category'];
                    var recommender = data['reco'];
                    $("#cate_ui").attr("src", "./images/img_" + cate_ui + ".png");

                    for (key in recommender) {
                        var listval = recommender[key]
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
                    //alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    alert("정보 등록 후 이용해주세요")
                }
            });
            togglecount++;
            $("input:checkbox[id='recotoggle']").prop("checked", true);
            chrome.browserAction.setPopup({ popup: "recommend_window.html" });
        });
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
            chrome.tabs.query({ 'active': true, 'lastFocusedWindow': true }, function (tabs) {
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
                var container = [];
                $.ajax({
                    type: "GET",
                    ContentType: 'application/json',
                    url: "http://127.0.0.1:8000/recommend/all/",
                    data: { fit: fit_data, url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
                    dataType: "json",
                    success: function (data) {
                        container = [];
                    
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
            
                $("#collapse-content").show("fast");
                
                $(document).on('click', '#del', function (){
                    //alert("clicked");
                    var tmp = $(this).parent().attr("id");
                    var del_data = tmp.replace(/[^0-9]/g, "");
                    container.splice(Number(del_data), 1);
                    paging((Object.keys(container).length) - 1, dataPerPage, pageCount, 1, container, index);
                    var cate = $("#cate_ui").attr("src");
                    cate = cate.replace(/[^A-Z]/g, "");
                    // alert(tmp)
                    $.ajax({
                        type: "DELETE",
                        ContentType: 'application/json',
                        url: "http://127.0.0.1:8000/recommend/delete/",
                        data: JSON.stringify({del_data : del_data, cate:cate, fit: fit_data}),
                        dataType: "json",
                        success: function (data) {                    
                            console.log("success");
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
        } else {
        $("#collapse-content").hide("fast");
        }
    });

    $("#tab1_trend").click(function () {
        $("#size-table-list *").remove();
        $("#size-table-info *").remove();
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
                url: "http://127.0.0.1:8000/recommend/trend/",
                data: { fit: '보통핏', url_send: encodeURIComponent(currentUrl), category_url: encodeURIComponent(categoryUrl) },
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
    $("#tab2_trend").click(function () {
        $("#size-table-list-large *").remove();
        $("#size-table-info-large *").remove();
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
    // $("#main-wrapper").hide();
    $("#register-container").hide();
    $("#like_container").hide();
    $("#size_container").hide();
    $("#recommend_container").hide();
    $("#clothes_category_input_container").hide();
    $("#clothes_size_input_container").hide();
    $("#clothes_fit_input_container").hide();
    $('#loading').hide();

});
