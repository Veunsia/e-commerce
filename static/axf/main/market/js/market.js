$(function () {
   $('.alltype').click(function () {
       $(this).find('span').toggleClass('glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up');
       $('#all_type_containt').toggle();
   });
   $('.sort_rule').click(function () {
       $(this).find('span').toggleClass('glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up');
       $('#sort_rule').toggle()
   });

   // $('.aaa').click(function () {
   //     $(this).find('span').toggleClass('a yellowSlide')
   // })
});