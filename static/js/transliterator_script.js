const form_section = document.getElementById("form-section")
const form_button = document.getElementById("form-button")
const reset_button = document.getElementById("reset")

window.addEventListener('load', (event) => {
    console.log("loaded")
    console.log(window.location.pathname)
    if (window.location.pathname =='/transliterator') {
        form_section.style.display = "none";
        reset_button.style.display = "block";}
    else {
        form_section.style.display = "block";
        reset_button.style.display = "none";}}
    )

    reset_button.onclick = function() {
        console.log("closing")
        form_section.style.display = "block";
        reset_button.style.display = "none";
        window.location.pathname = "/";
    }
