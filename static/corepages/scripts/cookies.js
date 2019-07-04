function getCookie(cname, verbose=true) {
    //console.log(`getCookie: requesting cookie ${cname}`)
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setCookie(cname, cvalue, exdays, verbose=true) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    if (verbose) console.log(`setCookie: cookie ${cname}=${cvalue}`)
}

function destroyCookie(cname, verbose=true) {
    if (verbose) console.log(`destroyCookie: destroying cookie ${cname}`)
    setCookie(cname, '', new Date(0).toUTCString())
}