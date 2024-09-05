let isNicknameValid = true


let url = window.location.href; // получаем текущий URL адрес
if (url.indexOf("settings") !== -1) { // проверяем, содержит ли URL слово "settings"
    $('#sidebar_label_wrapper1').addClass('sidebar_label_wrapper_active'); // добавляем класс "active" к элементу span
}
if (url.indexOf("settings/safety") !== -1) { // проверяем, содержит ли URL слово "safety"
    $('#sidebar_label_wrapper2').addClass('sidebar_label_wrapper_active'); // добавляем класс "active" к элементу span
}

/*
При нажатии кнопки изменить эта функция создает input для ввода никнейма и проверяет
его при помощи отправки данных на сервер через ajax запрос. После получения ответа
от сервера выводит результат
*/
$(document).ready(function () {
    // Создаем событие на кнопку 'Изменить'
    $("#changeButton").click(function () {
        // При нажатии превращаем элемент span в input
        const nickname = $("#nickname").text();
        const inputElement = $("<input/>", {
            id: "nicknameInput", class: "profile_main_card_username editable", type: "text", value: nickname,
        }).attr('maxlength', '20');
        $("#nickname").html(inputElement);

        const nicknameInput = $("#nicknameInput");
        const nicknameInputElement = nicknameInput[0];
        // Фокусируем на введенном значении
        nicknameInputElement.focus();
        nicknameInputElement.setSelectionRange(nicknameInputElement.value.length, nicknameInputElement.value.length);

        if (isNicknameValid === true && nicknameInput.css('background-color') !== 'rgba(123,200,86,0.3)') {
            nicknameInput.css('background-color', 'rgba(123,200,86,0.3)');
        }

        // А при потере фокуса меняем обратно на span
        nicknameInput.blur(function () {
            if (nicknameInput.val().length < 1) {
                ShowtextErrors(['Имя пользователя не может быть пустым'])
                change_usernameInput_bg(2)    //показать ошибки и покрасить инпут в красный
                isNicknameValid = false
                nicknameInput.focus();
            } else {
                const newValue = $(this).val();
                const newSpan = $("<span/>", {
                    id: "nicknameSpan", class: "profile_main_card_username", text: newValue,
                });
                $(this).replaceWith(newSpan);
            }
        });
        let timeoutId
        // Навешиваем событие change на nicknameInput
        nicknameInput.on('input', function () {
            clearTimeout(timeoutId); // Очищаем предыдущий timeout

            let username = $(this).val();
            const url = window.location.href;
            const csrftoken = getCookie('csrftoken');
            let delay = 300

            if (username.length > 0) {
                timeoutId = setTimeout(function () {
                    // Отправляем AJAX запрос на сервер
                    $.ajax({
                        url: url,
                        type: "POST",
                        headers: {'X-CSRFToken': csrftoken},
                        data: JSON.stringify({key: "check_username", username: username}),
                        dataType: "json",
                        contentType: "application/json;charset=utf-8",
                    })
                        .done(function (data) {
                            //Тексты ошибок находятся в файле валидатора в обработчике
                            if (data["is_username_valid"] === false) {
                                ShowtextErrors(data["username_errors"])
                                change_usernameInput_bg(2)    //показать ошибки и покрасить инпут в красный
                                isNicknameValid = false
                            }
                            if (data["is_username_valid"] === true) {
                                change_usernameInput_bg(1)    // перекрасить фон инпута на зеленый
                                isNicknameValid = true
                            }
                        })
                        .fail(function (jqXHR) {
                            ShowStatuscodeError(jqXHR.status)
                        });
                }, delay);
            }
        });
    });
});


// появление кнопки сохранить
$(document).ready(function () {
    $('.editable').on('input', function () {
        // Показать кнопку "сохранить"
        $('.save_changes_btn_container').css('display', "flex");
    });
});


function change_usernameInput_bg(color_index) {
    /*
    1 - green color
    2 - red color  */
    if (color_index === 1) {
        $(".profile_main_card_username").css('background-color', 'rgba(123,200,86,0.3)')
    }
    if (color_index === 2) {
        $(".profile_main_card_username").css('background-color', 'rgba(177,37,85,0.25)')
    }
}


/*______________load-image______________*/

$('.profile_main_card__img_container').on('click', function () {
    $('#img_input').click();
})
/*замена аватарки на фото, загруженное пользователем*/
$('#img_input').on('change', function (event) {
    let file = event.target.files[0];
    let reader = new FileReader();

    reader.onload = function (e) {
        $('.avatar').attr('src', e.target.result);
    };
    reader.readAsDataURL(file);
});

$('#gooey-button').on('click', function () {
    let avatar_img = $('.avatar')
    let username = $('.profile_main_card_username').val()

})