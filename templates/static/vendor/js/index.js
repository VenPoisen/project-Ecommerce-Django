var toggleStatus = 1;
var dropStatus = 1;
var dropDownStatus = 1;
var favoriteStatus = 1;

function dropRight() {
    if (dropStatus == 1 && toggleStatus == 0) {
        document.getElementById("navbarDropleft").style.display = "block";
        dropStatus = 0;
    }
    else if (dropStatus == 0 && toggleStatus == 0) {
        document.getElementById("navbarDropleft").style.display = "none";
        dropStatus = 1;
    }
};

function toggleMenu() {
    if (toggleStatus == 1) {
        document.getElementById("menu").style.left = "0";
        document.getElementById("block-outside").style.display = "block";
        toggleStatus = 0;
    }
    else if (toggleStatus == 0) {
        document.getElementById("menu").style.left = "-500px";
        document.getElementById("block-outside").style.display = "none";
        document.getElementById("navbarDropleft").style.display = "none";
        dropStatus = 1;
        toggleStatus = 1;
    }
};

function dropDown() {
    if (dropDownStatus == 1) {
        document.getElementById("profileDropDown").style.display = "block"
        dropDownStatus = 0
    }

    else if (dropDownStatus == 0) {
        document.getElementById("profileDropDown").style.display = "none"
        dropDownStatus = 1

    }
}

function getCEP() {

    $.ajax({
        type: 'GET',
        url: 'address/',
        data: {
            cep: $('#id_cep').val(),
            address: $('#id_address').val(),
            complement: $('#id_complement').val(),
        },
        success: function (data) {
            $('#id_address').attr('value', data.address);
            $('#id_neighborhood').attr('value', data.neighborhood);
            $('#id_city').attr('value', data.city);
            $('#id_state').attr('value', data.state);

            if (data.cep == undefined && data.address == undefined) {
                $("#div_id_cep").html(data);
                $("#submit-id-submit").prop("disabled", true)
            }
            else {
                $(document).on('change', ".is-invalid", function () {
                    $(this).removeClass('is-invalid');
                });
                $("#submit-id-submit").prop("disabled", false)
            }
            if (data.complement) {
                $('#id_complement').val(data.complement);
            }
        },
    })
}

function inputSelector() {
    $.ajax({
        type: 'GET',
        url: 'getaddress/',
        data: {
            inputSelect: $("#inputSelect").val(),
        },
        success: function (data) {

            if ($("#empty-address").attr("selected", false)) {

                document.getElementById("displayInput").classList.remove("d-none");

                address = document.getElementById("g-address");
                number = document.getElementById("g-number");
                complement = document.getElementById("g-complement");
                neighborhood = document.getElementById("g-neighborhood");
                city = document.getElementById("g-city");
                state = document.getElementById("g-state");
                cep = document.getElementById("g-cep");
                shipping_price = document.getElementById("shipping-price");
                cart_total = document.getElementById("cart-total");


                address.innerHTML = data.address;
                number.innerHTML = data.number;
                complement.innerHTML = data.complement;
                neighborhood.innerHTML = data.neighborhood;
                city.innerHTML = data.city;
                state.innerHTML = data.state;
                cep.innerHTML = data.cep;
                shipping_price.innerHTML = data.shipping_price_formatted;
                cart_total.innerHTML = data.cart_total;
            }
        }
    })
}

function cepCartCalculate() {
    $.ajax({
        type: 'GET',
        url: 'getcep/',
        data: {
            inputSelect: $("#id_cep").val(),
        },
        success: function (data) {
            $("#btn-cep-finder").css("cursor", "wait");
            valid_cep = data.price;
            error_msg = document.getElementById('error_msg_price');

            if (valid_cep == 'true') {
                error_msg.innerHTML = '';
                price = document.getElementById('cep-finder-price');
                price.innerHTML = data.shipping_price_formatted;

                document.getElementById('cep-results-cart').classList.remove('d-none');
            }
            if (valid_cep == 'false') {
                error_msg.innerHTML = 'Invalid CEP!';
                document.getElementById('cep-results-cart').classList.add('d-none');
            }

            setTimeout(function () {
                $("#btn-cep-finder").css("cursor", "pointer");
            }, 300);
        }
    })
}

function changeIconColor() {
    icon = document.getElementsByName('icon-delete-x');
    for (const i of icon) {
        i.classList.remove("text-danger");
    }
};

function clickRegister() {
    document.getElementById('register-form').classList.remove('d-none');
}