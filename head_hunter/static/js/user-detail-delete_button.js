// window.addEventListener('load', function() {
//
//
//
//     let buttonDelete = $('#btn-delete');
//     let modalDeleteConfirm = $('#myModalDeleteConfirm')
//
//     $('button[data-pk]').on('click', function(evt) {
//         const pk = $(this).data('pk')
//         console.log(pk)
//         evt.preventDefault()
//         modalDeleteConfirm[0].style.display = "block";
//     })
//
//     let buttonDeleteConfirm = $('#btn-delete-confirm');
//     let buttonDeleteCancel = $('#btn-delete-cancel');
//
//     buttonDeleteCancel.on('click', function(evt) {
//         evt.preventDefault()
//         modalDeleteConfirm[0].style.display = "none";
//     })
//
//     buttonDeleteConfirm.on('click', function(evt) {
//         evt.preventDefault()
//
//         const pk = $('button[data-pk]').data('pk')
//         let url = 'http://localhost:8000/resume/';
//         console.log(pk)
//         modalDeleteConfirm[0].style.display = "none";
//         $.ajax({
//             type: 'POST',
//             url : url + `${pk}/delete/`,
//             data: {
//                 csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//                 action:'post',
//             },
//             success: function(data) {
//
//                 alert(`Резюме ${pk} удалено!`)
//             }
//         })
//     })
// })