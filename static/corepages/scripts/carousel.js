// TODO auto switch slides if no user input
// TODO change links color based on current carousel page

let showSlide = (idx, loopthrough=false, automatic=false, stopAutoMode=true) => {

    // get vars
    $('#currentSlide')[0].classList.forEach( cls => {
        if (cls.match(/slide-(\d+)/)) {
            currentIndex = cls.replace(/slide-(\d+)/, ($0,$1)=>$1)
        }
    })
    slidesCount = $('[class*=slide-]').length
    currentIndex = parseInt(currentIndex)

    // determine target idx for relative navigation
    if (idx === '+') {
        idx = currentIndex + 1
    } else if (idx === '-') {
        idx = currentIndex - 1
    }

    if (loopthrough) {
        if (idx < 1) {
            idx = slidesCount
        } else if (idx > slidesCount) {
            idx = 1
        }
    }

    console.log(`showSlide/before: target=${idx} current=${currentIndex} slidesCount=${slidesCount}`)

    // handle prev/next dots
    if (idx === 1) {
        console.log(`showSlide: disable prev`)
        $('.dot-prev').addClass('disabled')
        $('.dot-next').removeClass('disabled')
    } else if (idx === slidesCount) {
        console.log(`showSlide: disable next`)
        $('.dot-next').addClass('disabled')
        $('.dot-prev').removeClass('disabled')
    } else {
        console.log(`showSlide: clear`)
        $('.dot-next').removeClass('disabled')
        $('.dot-prev').removeClass('disabled')
    }


    // switch IDs
    if (idx <= slidesCount && idx >= 1) {
        $('#currentSlide')[0].id = ''
        $('#currentDot')  [0].id = ''

        $(`.slide-${idx}`)[0].id = 'currentSlide'
        $(`.dot-${idx}`)  [0].id = 'currentDot'
    }

    // auto-cycle
    if (automatic) {
        intervalID = setInterval(() => {
            showSlide('+', true, false, false)
        }, 2000);
    } else if (stopAutoMode) {
        clearInterval(intervalID)
    }


}

if (document.body.classList.contains('body'))
    showSlide(1, true, true)