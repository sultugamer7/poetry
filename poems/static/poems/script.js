function show_hide(password, fa) {
    if ($('#'+password).get(0).type == 'password') {
        $('#'+password).get(0).type = 'text';
        $('.'+fa).addClass('fa-eye-slash').removeClass('fa-eye');
    } else {
        $('#'+password).get(0).type = 'password';
        $('.'+fa).addClass('fa-eye').removeClass('fa-eye-slash');
    }
}

function check(rate_id) {
    var n = parseInt(rate_id[rate_id.length - 1]);
    var rating_slected = parseInt(document.querySelector("#rating_slected").value);
    if (rating_slected < n) {
        document.querySelector("#my_rating").innerHTML = n+".0";
    }
    else {
        document.querySelector("#my_rating").innerHTML = rating_slected+".0";
    }
    for (i = 1; i <= n; i++) {
        $('#rate'+i).addClass('rate-check').removeClass('rate');
    }
}

function uncheck(rate_id) {
    var n = parseInt(rate_id[rate_id.length - 1]);
    var rating_slected = parseInt(document.querySelector("#rating_slected").value);
    document.querySelector("#my_rating").innerHTML = rating_slected+".0";
    for (i = rating_slected+1; i <= 5; i++) {
        $('#rate'+i).addClass('rate').removeClass('rate-check');
    }
}

function select_rating(rate_id) {
    var n = rate_id[rate_id.length - 1];
    var rating_selected = document.querySelector("#rating_slected");
    rating_selected.value = n+".0";
    for (i = 1; i <= 5; i++) {
        uncheck("rate"+i);
    }
}

// Run getRatings when DOM loads
document.addEventListener('DOMContentLoaded', getRatings);

// Get ratings
function getRatings() {
    if ($("#avg_user_rating").length > 0) {
        var avg_user_rating = document.getElementById("avg_user_rating").value;

        // Get percentage
        const starPercentage = (avg_user_rating / 5) * 100;

        // Round to nearest 10
        const starPercentageRounded = `${Math.round(starPercentage / 10) * 10.1}%`;

        // Set width of stars-inner to percentage
        document.querySelector(`.stars-inner`).style.width = starPercentageRounded;
    }
}