window.addEventListener('load', function() {

    let buttonWork= $('#add-modal-work');
    let modalWork = $('#myModal');
    buttonWork.on('click', function(evt) {
        modalWork[0].style.display = "block";
    });
    let pk = $("#resume").text();
    let buttonSaveWorkForm= $('#save-work');
    buttonSaveWorkForm.on('click', function(evt) {

        console.log($("#resume").text())
        modalWork[0].style.display = "none";
        evt.preventDefault();
        $.ajax({
            type: 'POST',
            url : 'create/experience/',
            data: {
                work_begin: $('#id_work_begin_year').val() + "-" + $('#id_work_begin_month').val() + "-" + $('#id_work_begin_day').val(),
                work_end: $('#id_work_end_year').val() + "-" + $('#id_work_end_month').val() + "-" + $('#id_work_end_day').val(),
                company: $('#id_company').val(),
                job_title: $('#id_job_title').val(),
                responsibilities: $('#id_responsibilities').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action:'post',
            },
            success: function(data) {

                alert('Опыт работы добавлен!')
            }
        })
    });

    let buttonCloseWork = $('#btn-close-work');
    buttonCloseWork.on('click', function(evt) {
        modalWork[0].style.display = "none";
    });




    let button_education = $('#add-modal-education');
    let modalEducation = $('#myModalEducation');
    button_education.on('click', function(evt) {
        modalEducation[0].style.display = "block";
    });

    let buttonSaveEducationForm= $('#save-education');
    buttonSaveEducationForm.on('click', function(evt) {
        modalEducation[0].style.display = "none";
        evt.preventDefault();
        $.ajax({
            type: 'POST',
            url : 'create/education/',
            data: {
                education_begin: $('#id_education_begin_year').val() + "-" + $('#id_education_begin_month').val() + "-" + $('#id_education_begin_day').val(),
                education_end: $('#id_education_end_year').val() + "-" + $('#id_education_end_month').val() + "-" + $('#id_education_end_day').val(),
                educational_institution_name: $('#id_educational_institution_name').val(),
                faculty: $('#id_faculty').val(),
                speciality: $('#id_speciality').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action:'post',
            },
            success: function(data) {

                alert('Сведения об образовании добавлены!')
            }
        })
    });

    let buttonCloseEducation = $('#btn-close-education');
    buttonCloseEducation.on('click', function(evt) {
        modalEducation[0].style.display = "none";
    });





    let button_courses = $('#add-modal-courses');
    let modalCourse = $('#myModalCourse');
    button_courses.on('click', function(evt) {
        modalCourse[0].style.display = "block";
    });

    let buttonSaveCourseForm= $('#save-course');
    buttonSaveCourseForm.on('click', function(evt) {
        modalCourse[0].style.display = "none";
        evt.preventDefault();
        $.ajax({
            type: 'POST',
            url : 'create/course/',
            data: {
                course_name: $('#id_course_name').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action:'post',
            },
            success: function(data) {

                alert('Сведения о курсах добавлены!')
            }
        })
    });

    let buttonCloseCourse = $('#btn-close-course');
    buttonCloseCourse.on('click', function(evt) {
        modalCourse[0].style.display = "none";
    });
});