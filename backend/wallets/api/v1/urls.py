from django.urls import path

from .views import WalletCreateView, WalletBalancView, WalletOperationView

app_name = 'wallets'

urlpatterns = [
    path('', WalletCreateView.as_view(), name='wallet-create'),
    path('<uuid:id>/', WalletBalancView.as_view(), name='wallet-balance'),
    path('<uuid:id>/operation', WalletOperationView.as_view(), name='wallet-operation'),
]
