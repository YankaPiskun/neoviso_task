from django.contrib import admin
from .models import Orders
from .models import Clients


admin.site.register(Orders)
admin.site.register(Clients)

