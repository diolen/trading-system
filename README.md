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

* используется **30 свечей (M15)**
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