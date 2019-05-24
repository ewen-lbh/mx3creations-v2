label = $('form label[for=id_bugreport]')
input = $('form input#id_bugreport')

// initial class 
applyClass()
// onclick
label.on('click', handleClick)

function applyClass() {
    state = input.checked
    if (state) {
        label.addClass('checked')
    } else {
        label.removeClass('checked')
    }
}

function handleClick() {
    // invert the state
    input.checked = !input.checked
    
    // apply the appropriate css class
    applyClass()
}