$(".ticket").on("click", function() {
    $(".ticket").removeClass("selected");

    $(this).addClass("selected");
    $("#donate").slideDown("slow");
    $("#donate-submit-button").attr("value", "BUY YOUR TICKET AND DONATE");
    setTotal();
});
$("#donate-button").on("click", function() {
    $("#donate").slideDown("slow");
    setTotal();
});
$("#search-button").on("click", function() {
    $("#search").slideDown("slow");
});

$("#datepicker").datetimepicker({
    format: "YYYY-MM-DD"
});

$(window).scroll(function () {
    if ($(this).scrollTop() != 0) {
    	$('#back-top').fadeIn();
    } else {
    	$('#back-top').fadeOut();
    }
});

$('#back-top').click(function() {
    $("html, body").animate({ scrollTop: 0 }, 600);
    return false;
});
