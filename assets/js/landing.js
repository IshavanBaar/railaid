$(".ticket").on("click", function() {
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
