(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_promo_price = document.getElementById('variation-price-promo');
    add_cart_btn = document.getElementById('add-cart-button');
    error_msg = document.getElementById('product-not-avaiable');
    qty_selector = document.getElementById('select-quantities');
    qty_avaiable = document.getElementById('qty_avaiable');

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

    if (!select_variation) {
        return;
    }
    else {
        insufficient_stock = select_variation.options[select_variation.selectedIndex].id;
        variation_stock = select_variation.options[select_variation.selectedIndex].getAttribute('stock');
        price = select_variation.options[select_variation.selectedIndex].getAttribute('data-price');
        price_promo = select_variation[select_variation.selectedIndex].getAttribute('data-price-promo');

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

        if (price) {
            variation_price.innerHTML = price;
            variation_promo_price.innerHTML = price_promo;
        }
        else {
            variation_price_none = document.getElementById('variation-price-none');
            variation_promo_price.innerHTML = price_promo;

            if (!variation_price_none) {
                variation_price.innerHTML = "";
            }
        }
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promo = this.options[this.selectedIndex].getAttribute('data-price-promo');
        variation_stock = this.options[this.selectedIndex].getAttribute('stock');
        insufficient_stock = this.options[this.selectedIndex].id;

        if (variation_price) {
            variation_price.innerHTML = price;
        }

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

(function () {
    detail_img = $('#prev-img-detail img');

    if (!detail_img) {
        return;
    }
    else {
        detail_img.click(function () {
            clicked_img_src = $(this).attr("src");
            active_img = $('.carousel-item.active');
            new_img = $('.carousel-item').find('[src="' + clicked_img_src + '"]');

            if (!new_img.parent().hasClass("active")) {
                active_img.removeClass('active');
                new_img.parent('div').addClass('active');
            }
        });
    }
})();

(function () {
    del_qty = document.getElementsByName('del-qty');

    if (del_qty.length === 0) {
        return;
    } else {
        item_qty = document.getElementsByName('item-qty');
        for (var i = 0; i < item_qty.length; i++) {
            qty_items_cart = item_qty[i].getAttribute('itemsQTY');

            for (var x = 1; x <= qty_items_cart; x++) {
                var opt = document.createElement('option');
                opt.value = x;
                opt.innerHTML = x;
                del_qty[i].appendChild(opt);
            }
        }
    }

})();

(function () {
    myForm = document.getElementsByName('delete-form');
    btn_icon = document.getElementsByName('button-delete-item');

    if (!myForm) {
        return;
    }

    if (!btn_icon) {
        return;
    }
    else {
        btn_icon_arr = Array.prototype.slice.call(btn_icon);

        for (const x of btn_icon) {
            x.addEventListener('click', function () {
                index_btn_icon = btn_icon_arr.indexOf(x);
                myForm[index_btn_icon].submit();
            })
        }
    }
})();

(function () {
    login_form = document.getElementById('login-form');
    register_form = document.getElementById('register-form');

    if (!login_form) {
        if (!register_form) {
            return;
        }
        else {
            document.getElementById('register-form').classList.remove('d-none');
        }
    }

    if (!register_form) {
        return;
    }
})();

(function () {
    track_order = document.getElementById("track");

    if (!track_order) {
        return;
    }
    else {
        order_status = document.getElementById("order_status");
        track_confirmed = document.getElementById("track_confirmed");
        track_pending = document.getElementById("track_pending");
        track_sent = document.getElementById("track_sent");
        track_finished = document.getElementById("track_finished");
        order_step = document.getElementById("order_step");

        if (order_status.innerText == "Created") {
            track_confirmed.classList.add("active");
            order_step.innerHTML = "Order created";
        }
        if (order_status.innerText == "Approved") {
            track_confirmed.classList.add("active");
        }
        if (order_status.innerText == "Pending") {
            track_confirmed.classList.add("active");
            track_pending.classList.add("active");
        }
        if (order_status.innerText == "Sent") {
            track_confirmed.classList.add("active");
            track_pending.classList.add("active");
            track_sent.classList.add("active");
        }
        if (order_status.innerText == "Finished") {
            track_confirmed.classList.add("active");
            track_pending.classList.add("active");
            track_sent.classList.add("active");
            track_finished.classList.add("active");
        }
        if (order_status.innerText == "Disapproved") {
            track_confirmed.classList.add("disapproved");
            document.getElementById('track_confirmed_dissaproved').classList.remove("fa-check");
            document.getElementById('track_confirmed_dissaproved').classList.add("fa-times");
            order_step.classList.add("text-red");
            order_step.innerHTML = "Order disapproved";
            document.getElementById("track_error").innerHTML = "There is an error with your order, please contact support";
        }
    }
})();