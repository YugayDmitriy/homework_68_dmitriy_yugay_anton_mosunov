window.addEventListener('load', function() {

    let buttonCloseResponse= $('#btn-close-response');
    let modalResponse = $('#modalResponse');
    buttonCloseResponse.on('click', function(evt) {
        modalResponse[0].style.display = "none";
    });


    let buttonResponse= $('#btn-response');
    buttonResponse.on('click', function(evt) {
        $('#id_message').val('Нас заинтересовало ваше резюме')
        modalResponse[0].style.display = "block";
    });

    let buttonSaveResponseForm= $('#save-response');
    buttonSaveResponseForm.on('click', function(evt) {
        modalResponse[0].style.display = "none";
        evt.preventDefault();
        $.ajax({
            type: 'POST',
            url : 'add/response/',
            data: {
                message: $('#id_message').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action:'post',
            },
            success: function(data) {

                alert('Ваш отклик добавлен!')
            }
        })

    })
})
