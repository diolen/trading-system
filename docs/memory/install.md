## Виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
which python
which pip
```

## Установка зависимостей
```bash
pip install ctrader-open-api pandas protobuf twisted
pip install OpenApiPy
```

## Итого:

| Что | Что это |
|-----|---------|
| OpenApiPy | Python SDK библиотека |
| trading-system (или любое имя) | твоё API приложение |
| client_id/client_secret | ключи доступа API

## Создай файл:
```
app/config/ctrader.py

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"

HOST = "demo.ctraderapi.com"
PORT = 5035

python test_connect.py
```

## Установить service_identity
Это warning, но лучше сразу исправить:
```bash
pip install service_identity
```