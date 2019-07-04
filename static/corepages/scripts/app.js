$(function() {
    ajaxifyLinks()
    initTypedJS()
})

window.onpopstate = event => {
    console.log('poped state to: '+document.location.pathname)
    changePage(document.location.pathname)
}

document.addEventListener('pageAJAXLoaded', event => {
    console.log('pageAJAXloaded')
    ajaxifyLinks('body #content a')
    initTypedJS()
    if ("fixURL" in window && document.body.classList.contains('fixURLs')) {
        console.log('fixing url')
        fixURL()
    }
})



initTypedJS = () => {
    if (document.body.classList.contains('typedjs')) {
        var typedTitle = new Typed("#typedjs_target", {
            stringsElement: "#typedjs_source",
            typeSpeed: 50,
            backSpeed: 25,
            backDelay:1800,
            cursorChar: '│',
            loop: true
        });
    } else {
        if ("typedTitle" in window) {
            typedTitle.destroy()
        }
    }
}

ajaxifyLinks = (selector='a') => {
    document.querySelectorAll(selector).forEach(link => {
        link.addEventListener('click', event => {
            url = link.getAttribute('href')
            if (url !== null    // if the href isn't empty
                && !url.match(/^https?:\/\//) // if it's not an external link
                && !url.match(/^#\w+/) // if it's not an in-page scroll with #
                && !link.classList.contains('noAJAX') // if we didn't manually disabled AJAXification
                ) {
                event.preventDefault()
                // Don't load the page anew if the link is the same
                if (url !== window.location.pathname) {
                    console.log(url)
                    changePage(url)
                } else {
                    closeAllSubMenus()
                    closeSearch()
                }
            }
        })
    })
    console.log('all links ajaxified!')
}

changePage = url => {
    $.ajax({
        type: 'GET',
        url: url,
        success: (data, textStatus, jqXHR) => handleSuccess(data, textStatus, jqXHR, url),
        error: (data, textStatus, jqXHR) => handleError(data, textStatus, jqXHR, url),
        dataType: 'html'
    })
}


handleSuccess = (data, textStatus, jqXHR, url) => {
    loadPage(data, url)
}

handleError = (data, textStatus, jqXHR, url) => {
    console.log('FUEEEEEEE')
    console.log(data)
    loadPage(data.responseText, url)
}


loadPage = (data, url) => {
    // close navbar
    closeSearch()
    closeAllSubMenus()

    // parse response to get window title, content,...
    let parser  = new DOMParser()
    let html    = parser.parseFromString(data, 'text/html')
    let pageTtl = $('head title', html)
    let content = $('#content', html)
    let bodycls = $('body', html)[0].classList

    // load the new data into the page
    $('body')[0].classList = bodycls
    document.title = pageTtl[0].innerText
    $('#content').html(content[0].innerHTML)

    // create history entry
    console.log(`loadPage: pushState with URL${url}`)
    history.pushState(history.state, document.title, url)

    // send custom event
    let event   = new Event('pageAJAXLoaded')
    document.dispatchEvent(event)
}

