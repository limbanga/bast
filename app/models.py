from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from slugify import slugify
from uuid import uuid4

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = RichTextField()
    stock = models.IntegerField(default=0)
    # foreign keys
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, null=True, default=None
    )

    def __str__(self) -> str:
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to="products", null=True, default=None)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    order = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Image for {self.product}"


class Category(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(_("slug"), max_length=50, unique=True)
    # foreign keys
    # one category can have one owner
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        slugName = slugify(self.name)
        uuid = uuid4().hex[:6].upper()
        self.slug = f"{slugName}-{uuid}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

CART_STATUS = (
    ("cart", "Cart"),
    ("order", "Order"),
    ("paid", "Paid"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


class Order(BaseModel):
    # foreign keys
    # the owner of the order
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    # the order lines for this order
    order_lines = models.ManyToManyField("OrderLine", related_name="order")
    # the status of the order
    status = models.CharField(choices=CART_STATUS, max_length=20, default="order")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_at = models.DateTimeField(null=True, default=None)
    completed_at = models.DateTimeField(null=True, default=None)

    def __str__(self) -> str:
        return f"Order by {self.owner} at {self.payment_at}"


class OrderLine(models.Model):
    # foreign keys
    # the product that this order line is for
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # the quantity of the product
    quantity = models.IntegerField()
    # the total price of the order line
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.product}"


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

    def __str__(self) -> str:
        return f"{self.rating} by {self.owner} for {self.product}"

class UserInformation(BaseModel):
    # foreign keys
    # the user that this information is for
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="information"
    )
    # the user's phone number
    phone = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to="avatars", null=True, default=None)
    # the user's address
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    cart_count = models.IntegerField(default=0)
    bio = models.CharField(max_length=64, null=True, default=None)
    reset_password = models.CharField(max_length=16, null=True, default=None)
    def __str__(self) -> str:
        return f"Information for {self.user}"


class Address(models.Model):
    # foreign keys
    # the owner of the address
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    # the address fields
    province = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    commune = models.CharField(max_length=255)
    extra_description = models.CharField(max_length=255, null=True, default=None)
