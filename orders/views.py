import json

from django.views    import View
from django.http     import JsonResponse
from json.decoder    import JSONDecodeError
from django.db       import transaction

from cart.models            import Cart
from users.models           import User
from products.models        import Product
from orders.models          import Order, OrderStatus, OrderItem, OrderItemStatus
from core.utils             import login_decorator

class OrderView(View):
    @login_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data         = json.loads(request.body)
            user         = request.user
            product_id   = data['product_id']
            order_status = data['order_status']
            order_id     = data['order_id']
            cart_id      = data['cart_id']
            cart         = Cart.objects.get(id=cart_id)
       
            if not Order.objects.filter(id=order_id).exists():
                Order.objects.create(
                        user = user,
                        product_id   = product_id,
                        order_status = order_status,
                )
            if not Delivery.objects.filter(id=deliveries_id).exists():
                Delivery.object.create(
                    address = address,

                        
                )
                cart_id = cart.get('cart_id', None)
                
                if cart_id:
                    cart.delete()    
                
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except JSONDecodeError :
            return JsonResponse({'message': "JSON_DECODE_ERROR"}, status=400)
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self , request):
        carts = Cart.objects.filter(user=request.user)
            
        result = [{
            'username'        : cart.user.username,
            'cart_id'         : cart.id,
            'product_id'      : cart.product.id,
            'title'           : cart.product.title,
            'quantity'        : cart.quantity,
            'price'           : cart.product.price,
            'thumbnail_images': cart.product.thumbnail_images.first().url,
            'discount'        : cart.product.discount,
            'stock'           : cart.product.stock,
            'total_price'     : int(cart.product.price) * int(cart.quantity),
            'mobile_number'   : cart.user.mobile_phone
            
        } for cart in carts]

        return JsonResponse({"result":result}, status = 200)