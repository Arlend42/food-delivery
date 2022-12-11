$(document).ready(function(){
    $('.remove_from_cart').on('click', function(e){
        e.preventDefault();
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        data = {
            product_id: product_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required!'){
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    });
                }
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-' +product_id).html(response.qty)
                    removeCartItem(response.qty, cart_id)
                }
            }
        })  
    })
       // delete the cart element if the quantity is 0
       function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // remove cart item element
            document.getElementById('cart-item-'+cart_id).remove()
        }
    }
      // place the cart item quantity on load
      $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#' + the_id).html(qty)
        console.log(qty)
    })
});