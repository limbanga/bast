from django.db import models

class BaseModel(models.Model): 
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  class Meta:
    abstract=True

class Product(BaseModel):
  name = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=5, decimal_places=2)
  description = models.TextField()