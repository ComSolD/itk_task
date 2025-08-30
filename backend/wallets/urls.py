from django.urls import path

from wallets.views import Test

app_name = 'wallets'

urlpatterns = [
    path('', Test.as_view())
]
