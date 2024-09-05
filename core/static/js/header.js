$(".header__avatar_wrapper__button").on("click", function () {

    const csrftoken = getCookie('csrftoken');
    const url = window.location.href;
    $.ajax({
        url: url,
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        data: JSON.stringify({"key": "is_authenticated"}),
        dataType: 'json',
        contentType: "application/json;charset=utf-8",
    })
        .done(function (data) {
            if (data['is_authenticated'] === false) {
                authorization_dialog_show();
            }
            if (data['is_authenticated'] === true) {
                $(".header__modal").css('display', 'block')
            }
        })
        .fail(function (data) {
            ShowStatuscodeError(data.status)
        })
})


jQuery(function ($) {
    $(document).mouseup(function (e) { // событие клика по веб-документу
        let div = $(".header__modal"); // тут указываем ID элемента
        if (!div.is(e.target) // если клик был не по нашему блоку
            && div.has(e.target).length === 0) { // и не по его дочерним элементам
            div.hide(); // скрываем его
        }
    });
});

$(document).on('keyup', function (e) {
    if (e.key === "Escape") {
        $(".header__modal").hide();
    }
});