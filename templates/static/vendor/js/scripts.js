(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_promo_price = document.getElementById('variation-price-promo');
    add_cart_btn = document.getElementById('add-cart-button');
    error_msg = document.getElementById('product-not-avaiable');

    if (!select_variation) {
        return;
    }
    else {
        insufficient_stock = select_variation.options[select_variation.selectedIndex].id;

        if (insufficient_stock == "insufficient-stock") {
            add_cart_btn.disabled = true;
            error_msg.innerHTML = "Sorry, we're temporarily out of stock";
        }
        else {
            add_cart_btn.disabled = false;
            error_msg.innerHTML = "";
        }
    }

    if (!variation_price) {
        return;
    }

    if (!add_cart_btn) {
        return;
    }

    if (!error_msg) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promo = this.options[this.selectedIndex].getAttribute('data-price-promo');
        insufficient_stock = this.options[this.selectedIndex].id;
        variation_price.innerHTML = price;

        if (variation_promo_price) {
            variation_promo_price.innerHTML = price_promo;
        }

        if (insufficient_stock == "insufficient-stock") {
            add_cart_btn.disabled = true;
            error_msg.innerHTML = "Sorry, we're temporarily out of stock";
        }
        else {
            add_cart_btn.disabled = false;
            error_msg.innerHTML = "";
        }
    })
})();

