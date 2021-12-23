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
            selector = document.getElementsByName(response.post_id);
            if(response.liked){
                var unlike = $(selector).attr('data-url').replace(split_url[3], 'unlike');
                $(selector).attr('data-url', unlike);
                $(selector).html("<i class='fas fa-lg fa-heart like-red'></i>");
            } else {
                var like = $(selector).attr('data-url').replace(split_url[3], 'like');
                $(selector).attr('data-url', like);
                $(selector).html("<i class='far fa-lg fa-heart'></i>");
            }
            selector2 = document.getElementsByName("count_" + response.post_id);
            $(selector2).text(response.count);
        }
    });
});
