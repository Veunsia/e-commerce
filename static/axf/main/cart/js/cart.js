$(function () {

    // market页面的加
    $('.addShopping').click(function () {
        var $button = $(this);
        var good_id = $button.attr('good_id');

        $.get('/axfcart/addToCart/',
            {'good_id': good_id},
            function (data) {
                if (data['status'] == 200) {
                    $button.prev('span').html(data['c_goods_num'])
                } else {
                    window.location.href = '/axfuser/login'
                }
            })
    });

    // market 页面的减
    $('.subShopping').click(function () {
        var $button = $(this);
        var good_id = $button.attr('good_id');

        $.get('/axfcart/subfromcart/',
            {'good_id': good_id},
            function (data) {
                if (data['status'] == 200) {
                    $button.next('span').html(data['c_goods_num'])
                } else if (data['status'] == 201) {
                    window.location.href = '/axfuser/login'
                }
            })
    });

    // 购物车页面的减
    $('.subgoods').click(function () {
        var $button = $(this);
        var $div = $button.parent().parent();
        var cartid = $div.attr('cartid');
        $.post(
            '/axfcart/subgoods/',
            {'cartid': cartid},
            function (data) {
                if (data['status'] == 200) {
                    $button.next('span').html(data['c_goods_num']);
                    $('.money').html(data['money'])
                } else {
                    $div.remove();
                    $('.money').html(data['money'])
                }
                if (data['isall']) {
                    $('.selectall').find('span').find('span').html('√');
                } else {
                    $('.selectall').find('span').find('span').html('');
                }
            }
        )
    });


    // 购物车页面的加
    $('.addgoods').click(function () {
        var $button = $(this);
        var $div = $button.parent().parent();
        var cartid = $div.attr('cartid');
        $.get(
            '/axfcart/addgoods/',
            {'cartid': cartid},
            function (data) {
                $button.prev('span').html(data['c_goods_num']);
                $('.money').html(data['money'])
            }
        )
    });

    // 单个的选择
    $('.isselect').click(function () {
        var $div = $(this);
        var cartid = $div.parent().attr('cartid');
        $.ajax({
            url: '/axfcart/isselect/',
            data: {'cartid': cartid},
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data['c_is_select'] == true) {
                    $div.find('span').find('span').html('√');
                } else {
                    $div.find('span').find('span').html('');
                }
                if (data['isall']) {
                    $('.selectall').find('span').find('span').html('√');
                } else {
                    $('.selectall').find('span').find('span').html('');
                }
                $('.money').html(data['money'])
            }
        })
    });


    // 全选
    $('.selectall').click(function () {
        var $div = $(this);
        $.get('/axfcart/selectall/',
            function (data) {
                // console.log(data);
                if (data['status'] == 200) {
                    $('.confirm').find('span').find('span').each(function () {
                        $(this).html('√')
                    });
                    $('.money').html(data['money'])
                } else {
                    $('.confirm').find('span').find('span').each(function () {
                        $(this).html('');
                    });
                    $('.money').html(data['money'])
                }
            })

    });


    // 下单
    $('.create_order').click(function () {
        var $span = $(this);
        $.get('/axforder/can_create/',
            function (data) {
                if (data['status'] == 201) {
                    return
                } else {
                    // console.log(data)
                    window.location.href = '/axforder/orderDetail/?order_id=' + data['order_id'];
                }
            })
    })


});