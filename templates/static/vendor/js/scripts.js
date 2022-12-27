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

        variation_preco.innerHTML = preco;

        if (variation_preco_promocional) {
            variation_preco_promocional.innerHTML = preco_promocional;
        }
    })
})();

