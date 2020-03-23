$(function () {
    var flog = false;
    var flog1 = false;

    $('#InputName').blur(function () {
        var name = $(this).val();
        var reg = /^\w{3,6}$/;
        var is_sure = reg.test(name);
        if (is_sure) {
            $.getJSON('/axfuser/checkname/',
                {'name': name},
                function (data) {
                    if (data['status'] == 200) {
                        $('.namehint').html(data['msg']).css({'color': 'green', 'font-size': '14px'});
                        flog = true;
                    } else {
                        $('.namehint').html(data['msg']).css({'color': 'red', 'font-size': '14px'});
                    }
                })
        } else {
            $('.namehint').html('用户名格式错误').css({'color': 'red', 'font-size': '14px'})
        }
    });

    $('#InputPassword2').blur(function () {
        var password1 = $('#InputPassword1').val();
        var password2 = $(this).val();
        if (password1 == password2) {
            $('.passwordhint').html('ok').css({'color': 'green', 'font-size': '14px'})
            flog1 = true;
        }else{
            $('.passwordhint').html('密码不一致').css({'color': 'red', 'font-size': '14px'})
        }
    });

    $('form').submit(function () {
        var b = flog & flog1;
        if(b==1){
            var password1 = $('#InputPassword1').val();
            password1 = md5(password1);
            $('#InputPassword1').val(password1);

            return true

        }else{
            $('.namehint').html('用户名格式错误').css({'color': 'red', 'font-size': '14px'});
            $('.passwordhint').html('密码不一致').css({'color': 'red', 'font-size': '14px'});
            return false
        }
    })
});