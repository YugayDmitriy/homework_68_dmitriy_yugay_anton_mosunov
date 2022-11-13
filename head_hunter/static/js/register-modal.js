window.addEventListener('load', function() {
    let button = $('#add-modal');
    let modal = $('#myModal');
    let form = $('.modal-content');
    button.on('click', function(evt) {
        modal[0].style.display = "block";

        let label = $('.form-label');
        let mb = $('.mb-3');
        let btn = $('.btn');

        for(let i=1; i < 7; i++) {
                label[i].style.display = "none";
                mb[i].style.display = "none";
            };
        btn[0].style.display = "none";

        let category_button = $('<input type="submit" class="btn btn-primary btn-sm" id="add-other-fields" value="Выбрать">')
        form.append(category_button)

        category_button = $('#add-other-fields')
        category_button.on('click', function(evt) {
            for(let i=1; i < 7; i++) {
                label[i].style.display = "block";
                mb[i].style.display = "block";
            }

            label[0].style.display = "none";
            mb[0].style.display = "none";

            btn[0].style.display = "block";
            category_button[0].style.display = "none";

            categ = $('#id_user_category')
            option = $("select option:selected").val();

            if (option == 'employer'){
                $('[for="id_username"]').text('Название компании');

            }
        });
    });
});