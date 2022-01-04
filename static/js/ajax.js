function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

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

$("[data-action='like']").on('click', function(event){
    event.preventDefault();
    const url = $(this).attr('data-url')
    const split_url = $(this).attr('data-url').split('/');
    const post_id = $(this).attr('data-store-id')
    const el = $(this)
    const like_css = "far fa-lg fa-heart"
    const unlike_css = "fas fa-lg fa-heart like-red"
    async function postData(){
        await fetch(url, {
            method: "POST",
            body: {
                'post_id': post_id
            },
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        }).then(response => {
            return response.json()
        }).then(response => {
            if(response.liked){
                const unlike = el.attr('data-url').replace(split_url[3], 'unlike');
                el.attr('data-url', unlike);
                el.children('i').attr('class', unlike_css)

            } else {
                const like = el.attr('data-url').replace(split_url[3], 'like');
                el.attr('data-url', like);
                el.children('i').attr('class', like_css)
            }
            count_selector = document.getElementsByName("count_" + post_id);
            $(count_selector).text(response.count);
        })
    }
    PostData()
});
