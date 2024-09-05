$('.header__profile_btn').on('click', function () {
    console.log("сработал клик")
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
            } else if (data['redirect_url']) {
                window.location.href = data['redirect_url'];  // выполнение редиректа
            }
        })
        .fail(function (data) {
            ShowStatuscodeError(data.status)
        })
})
