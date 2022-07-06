
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
from django.forms import CharField
from tags.models import TaggedItem


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product' ,on_delete=models.SET_NULL ,
        related_name='+' ,null=True ,blank=True)
    
    def __str__(self):
        return self.title

class VideoProduct(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class Product(models.Model):
    slug = models.SlugField(blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True ,blank=True)
    unit_price = models.DecimalField(max_digits=6 ,decimal_places=2 ,validators=[MinValueValidator(1 ,'low ... of 1.00')])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection ,on_delete=models.PROTECT ,related_name='collections')
    tag = GenericRelation(TaggedItem)
    videos = models.OneToOneField(VideoProduct, on_delete=models.CASCADE )


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Comment(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE ,related_name='comments') 
    name = models.CharField(max_length=255) 
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s'(self.post.title , self.name)




class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birthdate = models.DateField(null=True ,blank=True)
    
    MEMBERSHIP_BRONZE = 'B' 
    MEMBERSHIP_SILVER = 'S' 
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES =  [
        (MEMBERSHIP_BRONZE ,'Bronze') ,
        (MEMBERSHIP_SILVER ,'Silver') ,
        (MEMBERSHIP_GOLD , 'Gold'),
    ]

    membership = models.CharField(max_length=1 ,choices=MEMBERSHIP_CHOICES ,
        default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'





class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    places_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,validators=[MinValueValidator(1 ,'low...of 1')])
class Address(models.Model):
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    customer = models.OneToOneField(Customer ,on_delete=models.CASCADE ,
        primary_key=True)

        


# Create your models here.
