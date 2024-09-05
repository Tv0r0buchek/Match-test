function authorization_dialog_show() {
    $("body").css('overflow', 'hidden')
    $(".modal_background").css('display', 'flex')
}

$(document).ready(function () {
    // Закрытие блока при клике за его пределами
    $(document).click(function (event) {
        if (!$(event.target).closest('.modal_rectangle').length) {
            $('.modal_background').hide();
            $("body").css('overflow', '')
        }
    });

    // Закрытие блока по нажатию кнопки "Esc"
    $(document).keyup(function (event) {
        if (event.keyCode === 27) { // Код клавиши "Esc"
            $('.modal_background').hide();
            $("body").css('overflow', '')
        }
    });
});