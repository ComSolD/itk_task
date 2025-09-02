## Эндпоинты API

### Создать кошелек

`POST /api/v1/wallets/`

**Пример ответа:**

``` json
{
  "wallet": "7d8624f6-5820-41d3-9a9f-e70deb259438",
  "balance": "0"
}
```

------------------------------------------------------------------------

### Получить баланс кошелька

`GET /api/v1/wallets/{WALLET_UUID}/`

**Пример ответа:**

``` json
{
  "balance": "150.00"
}
```

------------------------------------------------------------------------

### Провести операцию

`POST /api/v1/wallets/{WALLET_UUID}/operation/`

**Тело запроса:**

``` json
{
  "operation_type": "DEPOSIT",
  "amount": 100
}
```

**Пример ответа:**

``` json
{
  "operation_id": "c5fbbf4b-2b9e-4dd0-9f65-3c86e8a96d2d",
  "operation_type": "DEPOSIT",
  "amount": "100.00",
  "created_at": "2025-09-01T12:00:00Z",
}
```

## Особенности

-   Баланс хранится в таблице `Wallet`, но каждая операция фиксируется в
    `Operation`.
-   Для защиты от гонок транзакций используется `transaction.atomic()` и
    `select_for_update()`.
-   Все настройки базы и приложения вынесены в `.env`.

## Пример содержимого `.env` файла:
```env
SECRET_KEY=supersecretkey

POSTGRES_DB=walletdb
POSTGRES_USER=walletuser
POSTGRES_PASSWORD=walletpass
POSTGRES_HOST=localhost # для .env.docker значение равно db
POSTGRES_PORT=5432
```
