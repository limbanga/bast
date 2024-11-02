from django.contrib import admin
from .models import *


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Review)
admin.site.register(UserInformation)
admin.site.register(ProductImage)


admin.site.site_header = "Bast Admin"

