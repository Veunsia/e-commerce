$('#pay').click(function () {
    var total_money = $('#total_price').html();
    var order_id = $(this).prev().prev().prev().html();
    // alert(order_id);
    window.location.href = '/axforder/testpay/?total_money=' + total_money +'&order_id=' + order_id
});