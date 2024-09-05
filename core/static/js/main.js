
function getCookie(name) {        // Получает csrf токен для выполнения ajax запроса
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function ShowStatuscodeError(status_code) {
    status_code = parseInt(status_code);


    let modal = document.querySelector('.statuscode_error_modal');
    modal.classList.add('showError'); // Добавить класс, активирующий анимацию
    setTimeout(function () {
        modal.classList.remove('showError');
    }, 6000); // Удалить класс, вызывающий анимацию, после окончания
    if (status_code) {
        $(".statuscode_error_modal_text").text("Ошибка, попробуйте позже, код " + status_code);
    } else {
        $(".statuscode_error_modal_text").text("Ошибка сервера, попробуйте позже");
    }
}

function ShowtextErrors(error_text) {
    let modal = document.querySelector('.text_errors_modal');
    modal.classList.add('showError'); // Добавить класс, активирующий анимацию
    setTimeout(function () {
        modal.classList.remove('showError');
    }, 7000); // Удалить класс, вызывающий анимацию, после окончания

    if (error_text && error_text.length > 0) {
        $(".text_error_label").text(""); // Очистить текст перед выводом новых ошибок
        error_text.forEach(function (error) {
            $(".text_error_label").append(error + "<br>"); // Вывести каждую ошибку на новой строке
        });
    } else {
        $(".text_error_label").text("Ошибка сервера, попробуйте позже");
    }
}


