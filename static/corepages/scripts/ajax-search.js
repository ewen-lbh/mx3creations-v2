$(function() {
$('#search').keyup(() => {
    $('#search-results').html(
        '<p class="status searching"> Searching... </p>'
    )
    setCookie('csrftoken', $('input[name=csrfmiddlewaretoken]').val(), 1, false)
    $.ajaxSetup({
        beforeSend: (xhr, settings) => {
            if (!this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val())
            }
        }
    })
    $.ajax({
        type: 'POST',
        url: '/search/',
        data: {
            q: $('#search').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            AJAX: true
        },
        success: loadSearchResults,
        dataType: 'html'
    })
})
})

loadSearchResults = (data, textStatus, jqXHR) => {
    $('#search-results').html(data)
    ajaxifyLinks()
}

