window.addEventListener('load', function() {
    let button = $('#add-modal');
    let modal = $('#myModal');
    let form = $('.modal-content');
    button.on('click', function(evt) {
        console.log(modal[0])
        modal[0].style.display = "block";

    });
});