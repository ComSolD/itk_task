from rest_framework import serializers
from wallets.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['operation_type', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Сумма меньше нуля')
        return value

    def validate_operation_type(self, value):
        if value not in ('DEPOSIT', 'WITHDRAW'):
            raise serializers.ValidationError('Неизвестный тип операции')
        return value
