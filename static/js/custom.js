$(document).ready(function () {

    $('.increment-btn').click(function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var max_inc_value = $(this).closest('.product_data').find('.max-qty').val();
        var value = parseInt(inc_value, 10);
        var max_value = parseInt(max_inc_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value < max_value) //10 gibt Wert an bis zu welcher Menge bestellt werden kann (nach 10 gehz Zähler nicht weiter hoch)
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        } else {
            alertify.error("Not more products in stock")

        }
    });

    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token

            },
            dataType: "",
            success: function (response) {
                alertify.success(response.status)

            }

        });
    });

    $('.changeQuantity').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token

            },
            dataType: "",
            success: function (response) {
                // alertify.success(response.status)

            }

        });
    });

    $(document).on('click', '.delete-cart-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token

            },
            success: function (response) {
                alertify.success(response.status)
                $('.cartdata').load(location.href + " .cartdata");
                // window.location.reload();
            }
        });
    });

    $('.addToWishlist').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token

            },
            dataType: "",
            success: function (response) {
                alertify.success(response.status)

            }

        });
    });

    $(document).on('click', '.delete-wishlist-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token

            },
            success: function (response) {
                alertify.success(response.status)
                $('.wishlistdata').load(location.href + " .wishlistdata");
            }
        });
    });

    $('#select1').change(function () {
        var option_value = $('#select1 option:selected').text();
        $('#result').val(option_value);
        console.log(option_value)
        var cat_slug = $(this).closest('.data-div').find('.cat_slug').val();
        console.log(cat_slug)
        var token = $('input[name=csrfmiddlewaretoken]').val()
        var filter = option_value.toLowerCase()

        $.ajax({
            type: "POST",
            url: '/collections/'+cat_slug,
            data: {
                'option_value': option_value,
                csrfmiddlewaretoken: token,
                'filter': filter,
            },
            success: function (response) {
                alertify.success(response.status)
                $('.prod-row').load(location.href + ' .prod-row');
                // $('.prod-row').load(location.href);
                // window.location.reload();
            }})
        });


    });