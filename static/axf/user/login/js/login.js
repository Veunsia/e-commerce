$(function () {
    var flag = false;
    var flag1 = false;

    $('#InputName').blur(function () {
        var name = $(this).val();
        $.getJSON('/axfuser/checklogin/',
            {'name': name},
            function (data) {
                if (data['status'] == 200) {
                    $('.namehint').html(data['msg']).css({'color': 'green', 'font-size': '14px'});
                    flag = true;
                } else {
                    $('.namehint').html(data['msg']).css({'color': 'red', 'font-size': '14px'});
                }
            })
    });

    $('form').submit(function () {
        var password = $('#InputPassword').val();
        if(password){
            flag1 = true;
            password = md5(password);
            $('#InputPassword').val(password)
        }else{
            $('.passwordhint').html('请输入密码').css({'color': 'red', 'font-size': '14px'});
        }
    });

    $('form').submit(function () {
        var b = flag & flag1;
       if(b == 1){
           return true
       }else{
           $('.namehint').html('请输入用户名').css({'color': 'red', 'font-size': '14px'});
           $('.passwordhint').html('请输入密码').css({'color': 'red', 'font-size': '14px'});
           return false
       }
    });
});


function change_code(){
    var i = document.getElementById('icode');
    i.src = '/axfuser/get_code/?'+Math.random();
}
