import pytest
from django.urls import reverse
from wallets.models import Wallet


@pytest.mark.django_db
def test_create_wallet(client):
    url = reverse("wallets:wallet-create")
    response = client.post(url)

    assert response.status_code == 200
    assert "Кошелек" in response.data["message"]
    assert Wallet.objects.count() == 1


@pytest.mark.django_db
def test_get_wallet_balance(client):
    wallet = Wallet.objects.create(balance=1337)
    url = reverse("wallets:wallet-balance", kwargs={"id": wallet.id})
    response = client.get(url)

    assert response.status_code == 200
    assert "1337" in response.data["message"]


@pytest.mark.django_db
def test_wallet_not_found(client):
    fake_wallet = "7d8624f6-5820-41d3-9a9f-e70deb159428"
    url = reverse("wallets:wallet-balance", kwargs={"id": fake_wallet})
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_operation_wallet_not_found(client):
    fake_wallet = "7d8624f6-5820-41d3-9a9f-e70deb159428"
    url = reverse("wallets:wallet-operation", kwargs={"id": fake_wallet})
    data = {"operation_type": "DEPOSIT", "amount": 322}
    response = client.post(url, data, fromat="json")

    assert response.status_code == 404


@pytest.mark.django_db
def test_deposit_operation(client):
    wallet = Wallet.objects.create(balance=0)
    url = reverse("wallets:wallet-operation", kwargs={"id": wallet.id})
    data = {"operation_type": "DEPOSIT", "amount": 420}
    response = client.post(url, data, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 200
    assert wallet.balance == 420


@pytest.mark.django_db
def test_withdraw_operation(client):
    wallet = Wallet.objects.create(balance=777)
    url = reverse("wallets:wallet-operation", kwargs={"id": wallet.id})
    data = {"operation_type": "WITHDRAW", "amount": 222}
    response = client.post(url, data, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 200
    assert wallet.balance == 555


@pytest.mark.django_db
def test_withdraw_not_enough_balance(client):
    wallet = Wallet.objects.create(balance=42)
    url = reverse("wallets:wallet-operation", kwargs={"id":wallet.id})
    data = {"operation_type": "WITHDRAW", "amount": 52}
    response = client.post(url, data, format="json")
    wallet.refresh_from_db()

    assert response.status_code == 400
    assert wallet.balance == 42


@pytest.mark.django_db
def test_invalid_operation_type(client):
    wallet = Wallet.objects.create(balance=430)
    url = reverse("wallets:wallet-operation", kwargs={"id":wallet.id})
    data = {"operation_type": "TESTTYPE", "amount": 21}
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert "operation_type" in response.data


@pytest.mark.django_db
def test_negative_amount(client):
    wallet = Wallet.objects.create(balance=1984)
    url = reverse("wallets:wallet-operation", kwargs={"id":wallet.id})
    data = {"operation_type": "TESTTYPE", "amount": -451}
    response = client.post(url, data, format="json")

    assert response.status_code == 400
    assert "amount" in response.data