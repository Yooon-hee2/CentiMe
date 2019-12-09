$('#submit').click(function () {
    fit = $("input[name=fit]:checked").val();
    size = $('#size').val();
    $.ajax({
        type: "POST",
        ContentType: 'application/json',
        url: "http://127.0.0.1:8000/info/store/",
        data: JSON.stringify({fit : fit, size : size}),
        dataType: "json",
        success: function (data) {
            console.log(data);
        },
        failure:
            function (err) {
                console.log(err);
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
             }
   
    });
});

