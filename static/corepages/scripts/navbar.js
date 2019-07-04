function toggleSubMenu(what) {
    other = what === 'creations' ? 'about' : 'creations'
    // toggle class
    $(`#navbar li.${what} .submenu`).toggleClass('opened')
    // close other submenu if we are opening this one
    if ($(`#navbar li.${other} .submenu`).hasClass('opened')) {
        $(`#navbar li.${other} .submenu`).removeClass('opened')
    }
    // handle .submenu-opened
    if ($(`#navbar li.${other} .submenu`).hasClass('opened') 
        || $(`#navbar li.${what}  .submenu`).hasClass('opened')){
        $('#navbar').addClass('submenu-opened')
        closeSearch()
    } else {
        $('#navbar').removeClass('submenu-opened')
    }
    // handle .hold-hover
    if ($(`#navbar li.${what} .submenu`).hasClass('opened')) {
        $(`#navbar li.${what} a`).addClass('hold-hover')
    } else {
        $(`#navbar li.${what} a`).removeClass('hold-hover')
    }
        if ($(`#navbar li.${other} .submenu`).hasClass('opened')) {
        $(`#navbar li.${other} a`).addClass('hold-hover')
    } else {
        $(`#navbar li.${other} a`).removeClass('hold-hover')
    }

    //handle btn-highlight passing through
    if ($('#navbar').hasClass('submenu-opened')) {
        document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
            e.style.zIndex = '-1'
        })
    } else {
        setTimeout(() => {
            document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
                e.style.zIndex = 'auto'
            })                
        }, 125);
    }
}

function toggleMenu() {
    opened = $('#navbar').hasClass('opened')
    if (opened) {
        $('#navbar').removeClass('opened')
        closeAllSubMenus()
        setTimeout(() => {
            document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
                e.style.zIndex = 'auto'
            })                
        }, 125);
    } else {
        $('#navbar').addClass('opened')
        document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
            e.style.zIndex = '-1'
        })
    }
}

function closeAllSubMenus() {
    $('#navbar').removeClass('submenu-opened')
    $('#navbar li .submenu').removeClass('opened')
    $('#navbar li a').removeClass('hold-hover')
}

function openSearch() {
    $("#navbar").addClass('search-opened')
    document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
        e.style.zIndex = '-1'
    })
    closeAllSubMenus()
}

function closeSearch() {
    $('#navbar').removeClass('search-opened')
    if(!$('#navbar').hasClass('submenu-opened')) {
        setTimeout(() => {
            document.querySelectorAll('.btn-highlight, .hide-on-navbar-open').forEach(e => {
                e.style.zIndex = 'auto'
            })                
        }, 125);
    }
    $('#search').val('')

}

$(document).keyup(e => {
    if (e.keyCode === 27 
        && ($('#navbar').hasClass('search-opened') 
            || $('#navbar').hasClass('submenu-opened')
        )
    ) {
        e.preventDefault()
        closeAllSubMenus()
        closeSearch()
    } else {
        if ($('#search').val() !== '') {
            openSearch()
        } else {
            closeSearch()
        }
    }
});

document.addEventListener('click', event => {
    // if we clicked outside of the navbar
    if (!$('#navbar')[0].contains(event.target)
        && ($('#navbar').hasClass('search-opened') 
            || $('#navbar').hasClass('submenu-opened')
        )
    ) {
        //event.preventDefault()
        closeAllSubMenus()
        closeSearch()
    }
})

document.addEventListener('scroll', ev => {
    headerHeight = parseInt(getComputedStyle($('#header')[0]).height.replace('px',''))
    if (window.pageYOffset > headerHeight) {
        $('#navbar').addClass('scrolled')
    } else {
        $('#navbar').removeClass('scrolled')
    }
})
