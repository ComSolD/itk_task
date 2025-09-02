from django.shortcuts import get_object_or_404, render
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OperationSerializer
from wallets.models import Wallet, Operation


class WalletCreateView(APIView):
    def post(self, request):

        wallet = Wallet.objects.create()

        return Response({"wallet": str(wallet.id), "balance": str(wallet.balance)}, status=status.HTTP_201_CREATED)


class WalletBalanceView(APIView):
    def get(self, request, id):

        wallet = get_object_or_404(Wallet, id=id)

        return Response({"balance": str(wallet.balance)})


class WalletOperationView(APIView):
    def post(self, request, id):
        serializer = OperationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            wallet = get_object_or_404(Wallet.objects.select_for_update(), id=id)

            operation_type = serializer.validated_data['operation_type']
            amount = serializer.validated_data['amount']

            if operation_type == 'WITHDRAW' and wallet.balance < amount:
                return Response({'error': 'Недостаточно средств'}, status=status.HTTP_400_BAD_REQUEST)

            operation = Operation.objects.create(
                wallet=wallet,
                operation_type=operation_type,
                amount=amount
            )

            if operation_type == 'DEPOSIT':
                wallet.balance += amount
            else:
                wallet.balance -= amount

            wallet.save()

        return Response({
            "operation_id": str(operation.id),
            "operation_type": operation.operation_type,
            "amount": str(operation.amount),
            "created_at": operation.created_at,
        }, status=status.HTTP_201_CREATED)
