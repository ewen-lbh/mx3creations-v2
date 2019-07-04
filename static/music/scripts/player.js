$(function() {
    $('#player-audio').on('ended', e => {
        loadTrack('+')
    })
})

function hex2RGBA(hex, cssFormat=false, opacity=1) {
    // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function(m, r, g, b) {
      return r + r + g + g + b + b;
    });
  
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    c = result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16),
      a: opacity
    } : null;
    if (cssFormat) {
        return `rgba(${c.r}, ${c.g}, ${c.b}, ${opacity})`
    } else {
        return c
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

fmtDuration2Secs = duration => {
    m = duration.split('<span class="time-separator">:</span>')[0]
    s = duration.split('<span class="time-separator">:</span>')[1]
    console.log(`m=${m} s=${s}`)
    return m + s*60
}


loadTrack = position => {
    OLD_PLAYER_TRACKLIST = PLAYER_TRACKLIST
    $('#player').removeClass('closed')

    currentPos = parseInt($('#player .player-data')[0].dataset.currentPosition)
    tracklist = OLD_PLAYER_TRACKLIST
    loopMode  = $('#player .player-data')[0].dataset.loopMode
    if (position === '+') {
        if (loopMode === 'track') {
            pos = currentPos
        } else {
            pos = currentPos + 1
        }
    } else if (position === '-') {
        if (loopMode === 'track') {
            pos = currentPos
        } else {
            pos = currentPos - 1
        }
    } else {
        pos = parseInt(position)
    }

    $('#player .next-track, #player .prev-track').removeClass('disabled')
    if (pos >= tracklist.length && loopMode === 'disabled') {
        $('#player .next-track').addClass('disabled')
    }
    if (pos <= 1 && loopMode === 'disabled') {
        $('#player .prev-track').addClass('disabled')
    }

    if (loopMode === 'tracklist') {
        if (pos > tracklist.length) {
            pos = 1
        } else if (pos < 1) {
            pos = tracklist.length
        }
    }

    if (!(pos < 1 || pos > tracklist.length)) {
        console.log(`loadTrack: requesting tracklist[${pos-1}]`)
        D = tracklist[pos-1]
        audioURL    = `/static/music/audio/${D.collection_slug}/${D.slug}.mp3`
        coverColor  = hex2RGBA(D.cover_accent, true, 001)
        coverColorT = hex2RGBA(D.cover_accent, true, 0.5)
        
        $('#player .play-pause i').removeClass('zmdi-play').addClass('zmdi-pause')
        $('#player .player-data')[0].dataset.currentPosition = pos
        $('#player .infos .title').text(D.title)
        $('#player .infos .collection').text(D.collection_title)
        $('#player .cover').css({
            backgroundImage: `url('/static/music/images/square/${D.collection_slug}.jpg')`
        })
        $('#player .cover, #player .collection').attr('href', `/listen/${D.collection_slug}`)
        document.title = `${D.artist} – ${D.title}`
        $('#player style.player-colors').html(
            [
            ':root {',
            `--player-accent: ${coverColor};`,
            `--player-accent-transparent: ${coverColorT};`
            ].join('\n')
        )
        $('#player .current-time').html('00<span class="time-separator">:</span>00')
        $('#player .total-time').html(D.duration.replace("'",'<span class="time-separator">:</span>'))
        $('#player .current-tracknum').text(pos)
        if (loopMode === 'disabled') {
            lastTrackNumDisplay = tracklist.length
        } else {
            lastTrackNumDisplay = '&infin;'
        }
        $('#player .last-tracknum').html(lastTrackNumDisplay)

        $('#player-audio').attr('src', audioURL)

        $('#player .play-pause i').removeClass('zmdi-pause')
                                  .addClass('zmdi-settings')
                                  .addClass('zmdi-hc-spin')
                                  .attr('onclick','')

        $('#player-audio').on('canplaythrough', e => {
            $('#player-audio')[0].play()

            $('#player .play-pause i').removeClass('zmdi-settings')
                                      .removeClass('zmdi-hc-spin')
                                      .addClass('zmdi-pause')
                                      .attr('onclick','playerToggle()')

            total_seconds=$('#player-audio')[0].duration
            setInterval(() => {            
                updatePlayer($('#player-audio')[0].currentTime, total_seconds)
            }, 500);
        })
    }


}

updatePlayer = (elapsed, total) => {
    elapsed = Math.floor(elapsed)
    updateCurrentTime(elapsed)
    updateTimeBar(elapsed, total)
}

updateCurrentTime = total_seconds => {
    s = total_seconds % 60
    m = Math.floor(total_seconds / 60)
    s = String(s).padStart(2, '0')
    m = String(m).padStart(2, '0')
    $('#player .time .current-time').html(`${m}<span class="time-separator">:</span>${s}`)
}

togglePlayer = () => {
    if ($('#player .play-pause i').hasClass('zmdi-pause')) {
        $('#player-audio')[0].pause()
    } else {
        $('#player-audio')[0].play()
    }
    $('#player .play-pause i').toggleClass('zmdi-play').toggleClass('zmdi-pause')
}

destroyPlayer = () => {
    $('#player-audio').attr('src','')
    $('#player').addClass('closed')
}

updateTimeBar = (elapsed, total) => {
    $('#player .time .time-bar').css({
        width: `calc(${elapsed / total} * 300px)`
    })
}

seekPlayer = offset => {
    $('#player-audio')[0].currentTime = $('#player-audio')[0].currentTime + offset
}

togglePlayerOpt = opt => {
    pdata = $('#player .player-data')[0]
    if (opt === 'loop') {
        currentLoopMode = pdata.dataset.loopMode
        switch (currentLoopMode) {
            case 'disabled':
                loopMode = 'tracklist'
                iconCls  = 'zmdi-repeat'
                break;

            case 'tracklist':
                loopMode = 'track'
                iconCls  = 'zmdi-repeat-one'
                break;
        
            default:
                loopMode = 'disabled'
                iconCls  = 'zmdi-repeat'
                break;
        }

        pdata.dataset.loopMode = loopMode


        if (loopMode === 'disabled') {
            $('#player .loop').addClass('disabled')
            lastTrackNumDisplay = PLAYER_TRACKLIST.length
        } else {
            $('#player .loop').removeClass('disabled')
            lastTrackNumDisplay = '&infin;'
        }

        $('#player .controls .loop i').removeClass('zmdi-repeat','zmdi-repeat-one').addClass(iconCls)
        $('#player .last-tracknum').html(lastTrackNumDisplay)
    }
}