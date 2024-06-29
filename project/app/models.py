from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model): 
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    abstract=True


class Product(BaseModel):  
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  description = models.TextField()
  # foreign keys
  # TODO: Remove null=True and default=None later
  owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)

  def __str__(self)->str:
    return self.name


class Category(BaseModel):
  name = models.CharField(max_length=255)
  description = models.TextField()
  # foreign keys
  # one category can have one owner
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  # one category can have many products
  products = models.ManyToManyField(Product, related_name='category', default=None)

  def __str__(self)->str:
    return self.name

class Order(BaseModel):
  # foreign keys
  # the owner of the order
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  # the order lines for this order
  order_lines = models.ManyToManyField('OrderLine', related_name='order')

  def __str__(self)->str:
    return f'Order by {self.owner} at {self.created}'

class OrderLine(models.Model):
  # foreign keys
  # the product that this order line is for
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  # the quantity of the product
  quantity = models.IntegerField()

  def __str__(self)->str:
    return f'{self.quantity} of {self.product}'

class Review(BaseModel):
  # foreign keys
  # the product that this review is for
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  # the owner of the review
  owner = models.ForeignKey(User, on_delete=models.CASCADE)
  # the rating of the product
  rating = models.IntegerField()
  # the review text
  review = models.TextField()

  def __str__(self)->str:
    return f'{self.rating} by {self.owner} for {self.product}'
