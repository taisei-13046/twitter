function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false,
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(event){
    $(document).on('click', '#like', function(event){
        event.preventDefault();
        var post_id = $(this).attr('name')
        $.ajax({
            type: 'POST',
            url: ,
            data: {
                'post_id': $(this).attr('name'),
                },
            dataType: 'json',
            success: function(response){
                selector = document.getElementsByName(response.post_id);
                if(response.liked){
                    $(selector).html("<i class='fas fa-lg fa-heart'></i>");
                }
                else {
                    $(selector).html("<i class='far fa-lg fa-heart'></i>");
                }
                selector2 = document.getElementsByName("count_" + response.post_id);
                $(selector2).text(response.count);
            }
        });
    });
});
