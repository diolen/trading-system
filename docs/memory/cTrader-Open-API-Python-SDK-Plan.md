Вот тебе **чёткий инженерный план** интеграции:

# 📊 cTrader Open API + Python SDK — Plan (v1 Integration)

Цель:
подключить твой `SignalEngine` к **живым M15 данным EURGBP** и довести до стадии “live signal generation”.

---

# 🧭 Общая архитектура

## Итоговая схема:

```text
cTrader Open API
        ↓
Python Market Data Client
        ↓
DataFrame Builder (M15 candles)
        ↓
SignalEngine
        ↓
Signal Output (print / log / future execution)
```

---

# 🪜 Этап 1 — Подготовка окружения (1 день)

## 1.1 Виртуальное окружение (починить)

Твоя ошибка с pip говорит, что venv сломан.

Сначала цель:

```bash
python3 -m venv venv
source venv/bin/activate
```

Проверка:

```bash
which python
which pip
```

---

## 1.2 Установка зависимостей

```bash
pip install ctrader-open-api pandas protobuf twisted
```

---

## 1.3 Проверка SDK

```python
import ctrader_open_api
print("OK")
```

---

# 🪜 Этап 2 — cTrader Connection Layer (2–3 дня)

## 2.1 Создать структуру

```text
app/
  data/
    ctrader_client.py   ← новый модуль
```

---

## 2.2 Ответственность модуля

Этот слой делает:

* OAuth authentication
* connection to cTrader server
* subscribe to symbols
* receive candles / ticks

---

## 2.3 Минимальная цель этапа

```text
print live EURGBP M15 candles
```

---

## 2.4 Результат этапа

Ты получаешь:

```python
[
  {"time": ..., "open": ..., "high": ..., "low": ..., "close": ...}
]
```

---

# 🪜 Этап 3 — Candle Builder (1–2 дня)

## 3.1 Задача

Преобразовать поток данных в:

```python
pd.DataFrame(columns=["open","high","low","close"])
```

с индексом:

```python
datetime
```

---

## 3.2 Требование

* строго M15
* без пропусков свечей
* обновление live

---

## 3.3 Результат

```text
live_df (rolling window)
```

---

# 🪜 Этап 4 — Подключение SignalEngine (1 день)

## 4.1 Просто подключаем:

```python
signal = engine.generate(df)
```

---

## 4.2 Важно

Ничего не менять в стратегии.

Только заменить источник данных:

```text
CSV → cTrader stream
```

---

## 4.3 Результат

Ты увидишь:

```text
TIME: ...
RANGE:
BREAKOUT: LONG/SHORT
SIGNAL: Signal(...)
```

---

# 🪜 Этап 5 — Signal Logging (1 день)

## 5.1 Добавить логирование

```text
logs/signals.json
```

или sqlite:

```text
signals.db
```

---

## 5.2 Записываем:

* entry
* stop
* tp
* timestamp
* direction

---

# 🪜 Этап 6 — Stabilization Layer (2–3 дня)

## Добавить:

### 6.1 reconnect logic

* потеря связи cTrader

### 6.2 duplicate candle protection

* защита от повторов

### 6.3 latency handling

* пропущенные свечи

---

# 🪜 Этап 7 — Paper Trading Mode (2–5 дней)

## Добавляется:

```text
signal → virtual execution engine
```

---

## Результат:

* PnL simulation
* win/loss tracking
* equity curve

---

# 🪜 Этап 8 — Live Execution (ПОСЛЕДНИЙ)

## Только после стабилизации:

```text
Signal → Order → cTrader
```

---

# 🧠 КРИТИЧЕСКАЯ АРХИТЕКТУРНАЯ ИДЕЯ

Твой `SignalEngine` уже идеален как:

```text
PURE STRATEGY LAYER
```

НЕ трогаем его под API.

---

# 📌 Что у тебя уже готово

✔ breakout logic
✔ retest logic
✔ session filter
✔ cooldown
✔ anti-repeat
✔ risk management
✔ signal model

---

# ⚠️ Основные риски (важно)

## 1. API complexity

cTrader = async + protobuf + OAuth

---

## 2. Candle correctness

самая частая ошибка:

* дубли свечей
* смещения времени

---

## 3. latency

M15 почти безопасно, но всё равно важно

---

# 🚀 Итоговый план (коротко)

## Завтра:

* починить venv
* установить SDK
* подключиться к cTrader
* вывести live candles

---

## Далее:

* собрать DataFrame stream
* подключить SignalEngine
* получить live сигналы

---

# 🧭 Финальная цель этапа

```text
LIVE EURGBP M15 STREAM → SIGNAL ENGINE → REAL SIGNALS
```

---

Если хочешь дальше — следующим шагом я могу:

👉 собрать тебе минимальный `ctrader_client.py` (готовый каркас под SDK)
👉 без лишней теории, сразу чтобы он коннектился и печатал свечи
