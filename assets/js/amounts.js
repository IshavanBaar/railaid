var oldAmount = $("#total-amount").val();
var donation_values = [];

function registerDonationValues() {
  donation_values = [];
  $(".donation-value").each(function() {
    donation_values.push($(this).val());
  });
}

registerDonationValues();
$("#total-amount").bind("keyup change", function() {
  if (isNaN(parseFloat($(this).val()))) {
    $(this).val(0);
  }

  var amount = $(this).val() ? parseFloat($(this).val()) : 0;

  $(".donation-value").each(function() {
    if (oldAmount == 0) {
      $(this).val((amount*1/4).toFixed(2));
    } else {
      $(this).val(($(this).val()*amount/oldAmount).toFixed(2));
    }
  });

  oldAmount = amount;
  registerDonationValues();
});

$(".donation-value").on("change", function() {
  var quotient = 1;
  var numberOfZero = 0;

  $(".donation-value").each(function(index, element) {
    if (isNaN(parseFloat($(this).val()))) {
      $(this).val("0");
    } else if (parseFloat($(this).val()) > parseFloat(oldAmount)) {
      $(this).val("" + oldAmount);
    }
    if ($(this).val() == "0") {
      numberOfZero += 1;
    }

    if (donation_values[index] != $(this).val()) {
      quotient = donation_values[index] - parseFloat($(this).val());
    }
  });

  $(".donation-value").each(function(index, element) {
    // 0 values are not changing
    if (donation_values[index] == $(this).val() && $(this).val() != "0") {
      $(this).val((parseFloat($(this).val()) + (quotient/(3 - numberOfZero))).toFixed(2));
    }

    donation_values[index] = $(this).val();
  });
});
