## 2026-05-12

## README.md
Вот обновлённый **README.md**, приведённый к согласованной **V1 стратегии (range = 30 свечей, price-based логика)** без лишнего усложнения:

---

# 📊 Trading System (Breakout + Retest Strategy)

Система генерации торговых сигналов на основе простой и формализованной логики:

* range (фиксированный диапазон)
* breakout (пробой)
* retest (подтверждение)
* базовый риск-менеджмент

---

## 🧠 Strategy Version

**Current version: V1 (baseline)**

Особенности:

* Range определяется по фиксированному количеству свечей
* Нет зависимости от ATR в логике диапазона
* Простая, детерминированная логика (подходит для отладки и масштабирования)

---

## ⚙️ Общая идея стратегии

Стратегия работает в 3 этапа:

### 1. Формирование диапазона (Range)

Берутся последние N свечей:

* `range_high = max(high)`
* `range_low = min(low)`
* `range_size = range_high - range_low`

Диапазон валиден, если:

* используется **90 свечей (M5)**
* размер диапазона ≥ минимального значения

---

### 2. Пробой (Breakout)

Сигнал пробоя возникает когда:

* цена закрывается выше `range_high` → LONG setup
* цена закрывается ниже `range_low` → SHORT setup

Дополнительно:

* свеча должна быть больше среднего размера последних свечей (фильтр импульса)

---

### 3. Ретест (Retest confirmation)

Вход только после подтверждения:

### LONG:

* цена возвращается к `range_high`
* не уходит глубже 30% диапазона
* следующая свеча закрывается вверх

### SHORT:

* зеркально

---

## ⏱️ Session Filter

Торговля ведётся только в активное время:

```text
08:00 – 12:00 UTC (London session)
```

---

## 📐 Риск-менеджмент

### Stop Loss:

```text
LONG:  range_high - buffer
SHORT: range_low + buffer
```

Где:

* `buffer = 5 pips`

---

### Take Profit:

```text
TP = entry ± (risk * RR)
```

Где:

* `RR = 2`

---

## 📏 Единицы измерения

Все расчёты ведутся через цену:

```text
1 pip = 0.0001
```

Пример:

* 15 pips = 0.0015
* 5 pips = 0.0005

---

## 🔁 Жизненный цикл сигнала

1. Build range (30 свечей)
2. Detect breakout (закрытие за пределами)
3. Wait retest (до 5 свечей)
4. Confirm entry
5. Generate signal
6. Reset

---

## 🧹 Фильтры

### 1. Минимальный размер диапазона

```text
>= 15 pips
```

---

### 2. Ограничение глубины ретеста

```text
не более 30% range
```

---

### 3. Время жизни ретеста

```text
максимум 5 свечей
```

---

## 📦 Модель сигнала

```python
@dataclass
class Signal:
    pair: str
    direction: str  # long / short
    entry: float
    stop: float
    tp: float
    timestamp: datetime
```

---

## 📁 Структура проекта

```
.
│
├── README.md
├── requirements.txt
├── generate_data.py
├── test_signal.py
├── .cursorrules
├── .gitignore
├── .windsurfignore
│
├── data/
│   └── (CSV файлы игнорируются .windsurfignore)
│
└── app/
    ├── main.py
    ├── config/
    │   └── settings.py
    ├── data/
    │   ├── data_provider.py
    │   └── dukascopy_loader.py
    ├── models/
    │   └── signal.py
    ├── strategy/
    │   ├── __init__.py
    │   ├── breakout.py
    │   └── signal_engine.py
    ├── bot/
    │   └── telegram_bot.py
    ├── storage/
    │   └── logger.py
    └── utils/
        └── __init__.py
```

**Примечание:** Файлы `__pycache__/`, `venv/`, `*.csv` и другие артефакты исключены из структуры согласно `.windsurfignore`.

---

## ⚙️ Основные параметры

```python
PAIR = "EURGBP"
TIMEFRAME = "M15"

PIP = 0.0001

RANGE_CANDLES = 30
MIN_RANGE_SIZE = 15 * PIP

RETEST_TOLERANCE = 3 * PIP
RETEST_DEPTH = 0.3
RETEST_MAX_CANDLES = 5

SL_BUFFER = 5 * PIP
RR_RATIO = 2
```

---

## ▶️ Запуск

```bash
python3 -m app.main
```

---

## ⚠️ Ограничения текущей версии

* нет ATR фильтра
* нет фильтра тренда
* нет spread/slippage
* нет полноценного backtest engine
* только базовая логика сигналов

---

## 🚀 Roadmap

### V2:

* ATR volatility filter
* false breakout detection
* multi-timeframe analysis

### V3:

* cTrader API integration
* полуавтомат / авто-исполнение

---

## 📌 Итог

Это минималистичная, но строгая breakout + retest система:

* без переусложнения
* с чёткими правилами
* готовая к кодированию и тестированию

---

## state.md
Вот **актуальный STATE твоего проекта (обновлённый по факту того, что у тебя уже есть + что ты только что добавил)**.

---

# 📊 STATE — Trading System + cTrader Integration (2026-05-12)

## 🧠 ОБЩАЯ СТАДИЯ

Проект находится в переходной фазе:

```text
BACKTEST ENGINE → LIVE MARKET DATA ENGINE
```

Ты уже вышел из стадии “стратегия как идея”
и находишься в стадии:

> ⚙️ “инфраструктура подключения к реальному рынку”

---

# ✅ ЧТО УЖЕ РАБОТАЕТ

## 🧠 1. CORE STRATEGY ENGINE (ГОТОВ)

### `SignalEngine`

✔ breakout detection
✔ retest confirmation
✔ session filter (UTC)
✔ cooldown logic
✔ anti-repeat levels
✔ range builder (30 candles)
✔ risk management (SL/TP RR=2)
✔ state machine (breakout → retest → signal)

📌 Статус:

```text
STABLE / PRODUCTION-READY (logic-wise)
```

---

## 📊 2. BREAKOUT STRATEGY (V2 EXPERIMENTAL)

### `BreakoutStrategy` (ATR version)

✔ ATR calculation
✔ volatility filter
✔ expanding volatility detection
✔ buffer-based breakout
✔ alternative signal model

📌 Статус:

```text
EXPERIMENTAL / PARALLEL RESEARCH LAYER
```

---

## 📦 3. DATA MODEL

### `Signal`

✔ structured dataclass
✔ entry / stop / tp
✔ timestamp
✔ pair / direction

📌 Статус:

```text
STABLE
```

---

## 📈 4. BACKTEST / SIMULATION MODE

✔ CSV-based DataFrame input
✔ deterministic execution
✔ reproducible signals

📌 Статус:

```text
WORKING (offline)
```

---

## 🧠 5. ARCHITECTURE PRINCIPLE

Ты уже разделил систему правильно:

```text
DATA → STRATEGY → SIGNAL → OUTPUT
```

И главное:

✔ стратегия не зависит от источника данных

---

# 🚧 ТЕКУЩИЙ ПЕРЕЛОМНЫЙ ЭТАП

## 🔌 6. MARKET DATA MIGRATION

Ты сейчас переходишь:

```text
CSV DATA
→ CTRADER OPEN API STREAM
```

---

## Что это означает архитектурно:

### ДО:

```text
pandas DataFrame (offline)
```

### СЕЙЧАС:

```text
live candle stream (async)
```

---

# ⚠️ ГЛАВНАЯ ПРОБЛЕМА СЕЙЧАС

Ты ещё не реализовал:

## ❌ Market Data Layer

Нет слоя:

```text
ctrader_client.py
```

который:

* подключается к API
* получает M15 candles
* формирует DataFrame
* обновляет stream

---

# 🧱 БУДУЩАЯ АРХИТЕКТУРА (ФАКТИЧЕСКАЯ)

## После интеграции cTrader:

```text
cTrader Open API
        ↓
Market Data Client (NEW)
        ↓
Candle Builder (NEW)
        ↓
SignalEngine (DONE)
        ↓
Signal Output (DONE)
```

---

# 🧠 ЧТО УЖЕ ХОРОШО СДЕЛАНО (ВАЖНО)

## 1. Strategy isolation ✔

Ты можешь менять источник данных без переписывания логики.

---

## 2. State machine ✔

Breakout → Retest → Signal уже работает как finite-state system.

---

## 3. Risk model ✔

RR / SL / TP уже встроены в ядро.

---

## 4. Session filter ✔

Лондонская сессия уже ограничивает шум.

---

## 5. Anti-repeat system ✔

Ты уже избегаешь повторных входов по уровню.

---

# 🧭 ГДЕ ТЫ НАХОДИШЬСЯ В РАЗВИТИИ

## Уровень зрелости:

```text
LEVEL 1: Strategy (DONE)
LEVEL 2: Backtest (DONE)
LEVEL 3: Live data integration (CURRENT)
LEVEL 4: Execution engine (NEXT)
LEVEL 5: Automation (FUTURE)
```

---

# ⚙️ ТЕХНИЧЕСКОЕ СОСТОЯНИЕ

## ❗ проблема окружения

* broken venv / pip
* pandas missing
* system Python conflict (PEP 668)

📌 это блокирует:

```text
live data testing
```

---

# 🧠 АРХИТЕКТУРНЫЙ ВЫВОД

Ты сейчас в самом важном переходе:

> из “алгоритма” → в “систему”

И ключевой момент:

✔ стратегия уже почти финальная
❗ инфраструктура только начинается

---

# 🚀 СЛЕДУЮЩИЙ РЕАЛЬНЫЙ ЭТАП (ФАКТ, НЕ РЕКОМЕНДАЦИЯ)

По состоянию проекта следующий логический шаг:

```text
cTrader Open API connection layer
```

---

# 📌 КОРОТКО

## Сейчас у тебя:

✔ working breakout system
✔ working retest logic
✔ working risk model
✔ working backtest
❌ no live data
❌ no API layer
❌ no execution

---

Если хочешь дальше — следующий шаг будет очень конкретный:

👉 собрать `ctrader_client.py` (минимальный live data connector без лишнего кода)


## cTrader-Open-API-Python-SDK-Plan.md
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
