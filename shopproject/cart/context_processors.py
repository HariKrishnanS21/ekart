from . models import Category,Product,Cart,CartItem
from .views import cart_id
def links(request):
    link=Category.objects.all()
    return dict(link=link)
def linksp(request):
    linkp=Product.objects.all()
    return dict(linkp=linkp)

def counter(request):
    item_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            car=Cart.objects.filter(cart_id=cart_id(request))
            cart_items=CartItem.objects.all().filter(car=car[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count=0
        return dict(item_count=item_count)
