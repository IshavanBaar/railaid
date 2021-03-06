var oldAmount = parseFloat($("#total-amount").val());
var donation_values = [];
var sliders = [];

$('.donation-value').each(function() {
  sliders[$(this).attr("name")] = $(this).slider({
  	formatter: function(value) {
  		return "£" + value;
  	}
  });

  // Slider events
  sliders[$(this).attr("name")].on("slide", function(e) {
    var quotient = 1;
    var numberOfZero = 0;
    var name = $(this).attr("name");

    $(".donation-value").each(function(index, element) {
      if (isNaN(parseFloat($(this).val()))) {
        setDonationValue($(this), "0");
      } else if (parseFloat($(this).val()) > parseFloat(oldAmount)) {
        setDonationValue($(this), "" + oldAmount);
      }
      if ($(this).val() == "0") {
        numberOfZero += 1;
      }

      if ($(this).attr("name") == name) {
        quotient = donation_values[index] - parseFloat($(this).val());
      }
    });

    if (numberOfZero === 4) {
      $(".donation-value").each(function(index, element) {
        setDonationValue($(this), (parseFloat($(this).val())/4).toFixed(2));
      });
    } else {
      $(".donation-value").each(function(index, element) {
        // 0 values are not changing
        if ($(this).attr("name") != name && $(this).val() != "0") {
          setDonationValue($(this), (parseFloat($(this).val()) + (quotient/(3 - numberOfZero))).toFixed(2));
        }

        donation_values[index] = $(this).val();
      });
    }
  });

  setTotal();
});

function registerDonationValues() {
  donation_values = [];
  $(".donation-value").each(function() {
    donation_values.push($(this).val());
  });
}

function setDonationValue(element, value) {
  element.val(value);
  sliders[element.attr("name")].slider('setValue', parseFloat(value));
  sliders[element.attr("name")].slider('setAttribute', 'value', parseFloat(value));
}

function getSum() {
  var sum = 0;
  $(".donation-value").each(function() {
    sum += parseFloat($(this).val());
  });
  return sum;
}

function setTotal() {
  sum = getSum();
  if ($(".ticket.selected .price-value").length > 0) {
    sum += parseFloat($(".ticket.selected .price-value").html());
  }

  $("#total-price").html(""+sum);
}

registerDonationValues();
$("#total-amount").bind("keyup change", function() {
  var amount = $(this).val() ? parseFloat($(this).val()) : 0;

  $(".donation-value").each(function() {
    if (oldAmount == 0) {
      setDonationValue($(this), ((amount*1/4).toFixed(2)));
    } else {
      setDonationValue($(this), (($(this).val()*amount/oldAmount).toFixed(2)));
    }
  });

  oldAmount = parseFloat(amount);

  for (var key in sliders) {
    sliders[key].slider('setAttribute', 'max', oldAmount);
    sliders[key].slider('refresh');
  }

  registerDonationValues();
  setTotal();
});
