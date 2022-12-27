(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_promo_price = document.getElementById('variation-price-promo');

    if (!select_variation) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('data-price');
        price_promo = this.options[this.selectedIndex].getAttribute('data-price-promo');

        variation_price.innerHTML = price;

        if (variation_promo_price) {
            variation_promo_price.innerHTML = price_promo;
        }
    })
})();

