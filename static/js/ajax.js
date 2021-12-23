function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).on('click', '#like', function(event){
    event.preventDefault();
    var url = $(this).attr('data-url')
    var post_id = $(this).attr('name')
    var split_url = $(this).attr('data-url').split('/');
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'post_id': post_id,
        },
        dataType: 'json',
        success: function(response){
            if(response.liked){
                var unlike = $(selector).attr('data-url').replace(split_url[2], 'unlike');
                console.log(unlike)
                $(selector).attr('data-url', unlike);
                $(selector).html("<i class='fas fa-thumbs-up'></i>");
            } else {
                var like = $(selector).attr('data-url').replace(split_url[2], 'like');
                $(selector).attr('data-url', like);
                $(selector).html("<i class='far fa-thumbs-up'></i>");
            }
            selector2 = document.getElementsByName("count_" + response.post_id);
            $(selector2).text(response.count);
        }
    });
});
