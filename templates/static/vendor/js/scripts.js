(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_promo_price = document.getElementById('variation-price-promo');
    add_cart_btn = document.getElementById('add-cart-button');
    error_msg = document.getElementById('product-not-avaiable');
    qty_selector = document.getElementById('select-quantities');
    qty_avaiable = document.getElementById('qty_avaiable')

    if (!select_variation) {
        return;
    }
    else {
        insufficient_stock = select_variation.options[select_variation.selectedIndex].id;
        variation_stock = select_variation.options[select_variation.selectedIndex].getAttribute('stock');

        if (insufficient_stock == "insufficient-stock") {
            add_cart_btn.disabled = true;
            error_msg.innerHTML = "Sorry, we're temporarily out of stock";
        }
        else {
            add_cart_btn.disabled = false;
            error_msg.innerHTML = "";
        }

        if (variation_stock < 1) {
            qty_avaiable.classList.add("d-none")
        }
        else {
            qty_avaiable.classList.remove("d-none")
            while (qty_selector.firstChild) {
                qty_selector.removeChild(qty_selector.firstChild);
            }
            for (var i = 1; i <= 25; i++) {
                var opt = document.createElement('option');
                opt.value = i;
                opt.innerHTML = i;
                qty_selector.appendChild(opt);
            }
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

    if (!qty_selector) {
        return;
    }

    if (!qty_avaiable) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promo = this.options[this.selectedIndex].getAttribute('data-price-promo');
        variation_stock = this.options[this.selectedIndex].getAttribute('stock');
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

        if (variation_stock < 1) {
            qty_avaiable.classList.add("d-none")
        }
        else {
            qty_avaiable.classList.remove("d-none")
            while (qty_selector.firstChild) {
                qty_selector.removeChild(qty_selector.firstChild);
            }
            for (var i = 1; i <= 25; i++) {
                var opt = document.createElement('option');
                opt.value = i;
                opt.innerHTML = i;
                qty_selector.appendChild(opt);
            }
        }
    })
})();

