window.addEventListener('load', function() {

    let buttonCloseResponse= $('#btn-close-response');
    let modalResponse = $('#modalResponse');
    buttonCloseResponse.on('click', function(evt) {
        modalResponse[0].style.display = "none";
    });


    let buttonResponse= $('#btn-response');
    buttonResponse.on('click', function(evt) {
        $('#id_hello_message').val('Здравствуйте. Нас заинтересовало ваше резюме!')
        modalResponse[0].style.display = "block";
    });

    let buttonSaveResponseForm= $('#save-response');
    buttonSaveResponseForm.on('click', function(evt) {
        modalResponse[0].style.display = "none";
        evt.preventDefault();
        console.log($('#id_vacancy').val())
        $.ajax({
            type: 'POST',
            url : 'add/response/',
            data: {
                hello_message: $('#id_hello_message').val(),
                vacancy: $('#id_vacancy').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action:'post',
            },
            success: function(data) {

                alert('Ваш отклик добавлен!')
            }
        })
    })
})
