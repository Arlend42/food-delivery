$(document).ready(function(){  
    // delete cart item
    $('.delete_cart_item').on('click', function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            cart_id: cart_id,
        }
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    swal(response.status, response.message, 'success')
                    removeCartItem(0, cart_id)
                    checkEmptyCart()
                }
            }
        })
    })
    // delete the cart element if the quantity is 0
    function removeCartItem(cartItemQt, cart_id){
        if(cartItemQt <= 0){
            // remove cart item element
            document.getElementById('cart-item-'+cart_id).remove()
        }
    }
    // check if the cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block';
        }
    }
});