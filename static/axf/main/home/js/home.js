$(function () {
    init_wheel();
    init_mustbuy();
});

function init_wheel() {
    var mySwiper = new Swiper('#topSwiper', {
        loop: true,
        pagination: '.swiper-pagination',
        autoplay: 2000,
        autoplayDisableOnInteraction: false
    });
}

function init_mustbuy() {
    var mySwiper = new Swiper('#swiperMenu',{
       slidesPerView:3,
    });
}