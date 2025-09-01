from django.contrib import admin

from .models import Wallet, Operation

admin.site.register(Wallet)
admin.site.register(Operation)
