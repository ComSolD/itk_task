import uuid
from django.db import models


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    class Meta():
        db_table = 'wallet'
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'


class Operation(models.Model):
    OPERATION_TYPE = [
        ('DEPOSIT', 'Взнос'),
        ('WITHDRAW', 'Вывод')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    operation_type = models.CharField(choices=OPERATION_TYPE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta():
        db_table = 'operation'
        verbose_name = 'Операция'
        verbose_name_plural = 'Операции'
