$(document).ready(function(){
    $('.sidenav').sidenav();
    $('.slider').slider({indicators:false, height:450});
    $('.timepicker').timepicker({
        default: 'now',
        twelveHour: false,
    });
    $('select').select();
});