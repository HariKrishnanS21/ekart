from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    img=models.ImageField(upload_to='category')

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('cart:pro_category',args=[self.slug])

    def __str__(self):
        return  '{}'.format(self.name)


class Product(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    img=models.ImageField(upload_to='product')
    desc=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stocks=models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    cdate=models.DateTimeField(auto_now_add=True)
    udate=models.DateTimeField(auto_now=True)
    availability=models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse('cart:prodetails',args=[self.category.slug,self.slug])

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date=models.DateField(auto_now_add=True)

    class Meta:
        ordering=['date']
        db_table=('Cart')

    def __str__(self):
        return '{}'.format(self.cart_id)

class CartItem(models.Model):
    pro=models.ForeignKey(Product,on_delete=models.CASCADE)
    car=models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    active=models.BooleanField(default=True)

    class Meta:
        db_table=('CartItem')

    def sub_total(self):
        return self.pro.price * self.quantity

    def __str__(self):
        return '{}'.format(self.pro)


