const form_section = document.getElementById("form-section")
const inputText = document.getElementById("inputText")
const form = document.getElementById("transliteratorForm")
const form_button = document.getElementById("form-button")
const reset_button = document.getElementById("reset")
const loader = document.getElementById("loader")


window.addEventListener('load', (event) => {
    console.log("loaded")
    console.log(window.location.pathname)
    if (window.location.pathname =='/transliterator') {
        form_section.style.display = "none";
        reset_button.style.display = "block";
        loader.style.display = "none";
    
    }
    else {
        form_section.style.display = "block";
        loader.style.display = "none";
    }
    }
    )

form_button.onclick = function() {
     if (form.checkValidity()){
        console.log("loading")
    form_section.style.display = "none";
    loader.style.display = "block";
    window.location.pathname = "/";
}
 }

reset_button.onclick = function() {
    console.log("closing")
     loader.style.display = "none";
     form_section.style.display = "none";
    window.location.pathname = "/";
}

