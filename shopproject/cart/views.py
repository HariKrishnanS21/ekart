from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from . models import Category,Product,Cart,CartItem
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request,'home.html')

def catpage(request,c_slug):
    c_page=None
    pro=None
    if c_slug != None:
        c_page=get_object_or_404(Category,slug=c_slug)
        pro=Product.objects.all().filter(category=c_page,availability=True)
    else:
        pro=Product.objects.all().filter(availability=True)
    paginator=Paginator(pro,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        product=paginator.page(page)
    except(EmptyPage,InvalidPage):
        product=paginator.page(paginator.num_pages)
    return render(request,'category.html',{'cat':c_page,'product':product})

def prodetails(request,c_slug,p_slug):
    try:
        pro=Product.objects.get(category__slug=c_slug,slug=p_slug)
    except Exception as e:
        raise e
    return render(request,'product.html',{'pro':pro})


def search(request):
    product=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        product=Product.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
        return render(request,'search.html',{'query':query,'product':product})


def cart_id(request):
    cart_s=request.session.session_key
    if not cart_s:
        cart_s=request.session.create()
    return cart_s

def add_cart(request,id):
    pro=Product.objects.get(id=id)
    try:
        car=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        car=Cart.objects.create(cart_id=cart_id(request))
        car.save()
    try:
        cart_item=CartItem.objects.get(pro=pro,car=car)
        if cart_item.pro.stocks >= 1:
            cart_item.quantity += 1
            cart_item.save()
            cart_item.pro.stocks -= 1
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(pro=pro,car=car,quantity=1)
        cart_item.save()
    return redirect('cart:cart_details')

def cart_details(request,total=0,counter=0,cart_items=None):
    try:
        car=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(car=car,active=True)
        for cart_item in cart_items:
            total += (cart_item.pro.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def item_remove(request,id):
    car=Cart.objects.get(cart_id=cart_id(request))
    pro=get_object_or_404(Product,id=id)
    cart_items=CartItem.objects.get(pro=pro,car=car)
    if cart_items.quantity > 1:
        cart_items.quantity -= 1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('cart:cart_details')


def remove(request,id):
    car = Cart.objects.get(cart_id=cart_id(request))
    pro = get_object_or_404(Product, id=id)
    cart_items = CartItem.objects.get(pro=pro, car=car)
    cart_items.delete()
    return redirect('cart:cart_details')



def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        u=auth.authenticate(username=username,password=password)

        if u is not None:
            auth.login(request,u)
            return redirect('cart:home')

        else:
            messages.error(request,"Invalid credentials")
            return redirect('cart:home')
    return render(request,'home.html')


def register(request):
    if request.method== 'POST':
        uname=request.POST['uname']
        password=request.POST['pass']
        cpass=request.POST['cpass']

        if password == cpass:
            if User.objects.filter(username=uname):
                messages.warning(request,"Username already exist")
                return redirect('cart:register')
            else:
                user=User.objects.create_user(username=uname,password=password)
                user.save()

        else:
            messages.warning(request,"passwords are not  matching")
            return redirect('cart:register')
        return redirect('cart:home')

    return render(request,'reg.html')

def logout(request):
    auth.logout(request)
    return redirect('/')