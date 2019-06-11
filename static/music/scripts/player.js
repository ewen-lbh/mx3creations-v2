function getPlayerInfos() {
    // Load cookies
    tPos = getCookie('playerPosition')
    tLen = getCookie('playerTotalTime')
    tState = getCookie('playerState')
    tURL = getCookie('playerURL')
    infos = getCookie('playerInfo')

    // getCookie returns "" when the cookie isn't set. 
    // Return null if any of the cookies aren't set
    if (!tPos || !tURL || !tLen || !infos) {
        return null
    }

    // decode JSON-encoded cookies
    infos = JSON.parse(infos)

    // Returns infos
    return {
        artist: infos.artist,
        kind: infos.kind,
        title: infos.title,
        track: infos.track,
        tracknum: infos.tracknum,
        position: parseInt(tPos),
        length: parseInt(tLen),
        resource: tURL,
        state: tState,
        _rawInfo: rawInfos
    }
}

function loadPlayer(data) {
    // Get DOM elements
    track = $('#player .title .track')[0]
    title = $('#player .title .from')[0]
    artist = $('#player .title .by')[0]
    playbtn = $('#player .controls .play-pause')
    console.log('loadPlayer: Got DOM elements')

    // Load in the audio
    let playerAudio = new Audio(data.resource)
    playerAudio.currentTime = data.position
    playerAudio.paused = data.state
    console.log('loadPlayer: Initialized Audio()')

    // Sets player texts
    track.innerText = data.track
    title.innerText = data.title
    artist = data.artist
    console.log('loadPlayer: Set player texts')

    // Sets play-pause button icon
    playerAudio.paused ? playbtn.addClass('play') : playbtn.addClass('pause')
    console.log('loadPlayer: Set player control play-pause icon')

    // init durations by running tickPlayer at least once
    tickPlayer(data)
    console.log('loadPlayer: first player tick')
    // start the loop (updates {#player .progress-bar}'s children)
    setInterval(() => {
        if (!playerAudio.paused) {
            tickPlayer(data)
        }
    }, 100);

}

function savePlayer() {
    // Get infos
    pos = $('#player .progress-bar .time-current')[0].dataset.seconds
    remaining = $('#player .progress-bar .time-remaining')[0].dataset.seconds
    url = $('#player')[0].dataset.resourceUrl


    // Set infos
    setCookie('playerPosition', pos, 1)
    setCookie('playerTotalTime', pos + remaining, 1)
    setCookie('playerURL', url, 1)
    setCookie('playerInfos', JSON.stringify(infos), 1)
}

function playerToggle() {
    elem = $('#player .controls .play-pause')
    if (playerAudio.paused) {
        playerAudio.play()
        elem.removeClass('pause')
        elem.addClass('play')
        console.log('playerToggle: toggled state to pause')
    } else {
        playerAudio.pause()
        elem.removeClass('play')
        elem.addClass('pause')
        console.log('playerToggle: toggled state to play')
    }
}

function tickPlayer() {
    function formatTime(seconds) {
        var date = new Date(null);
        date.setSeconds(seconds);
        var timeString = date.toISOString().substr(14, 5);
        return timeString
    }

    // Get DOM Elements
    eProgBar = $('#player .progress-bar .bar')
    eTimeCur = $('#player .progress-bar .time-current')[0]
    eTimeRem = $('#player .progress-bar .time-remaining')[0]

    // Update durations
    vTimeCur = playerAudio.currentTime
    eTimeCur.setAttribute('data-seconds', vTimeCur)
    eTimeCur.innerText = formatTime(vTimeCur)

    vTimeRem = playerAudio.duration - playerAudio.currentTime
    eTimeRem.setAttribute('data-seconds', vTimeRem)
    eTimeRem.innerText = formatTime(vTimeRem)

    // Update .progress-bar
    barW = vTimeCur / eProgBar.width * playerAudio.duration
    eProgBar.css({
        width: barW + 'px'
    })
}