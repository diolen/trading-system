Вот собранный **единый README.md** под текущее состояние твоего проекта (без воды, но с полной структурой того, что уже реализовано).

---

````markdown
# 📊 Trading System (Breakout + Retest Strategy)

Система генерации торговых сигналов на основе:
- range breakout
- retest подтверждения
- ATR volatility filter
- stateful engine (память рынка)

---

## ⚙️ Общая идея стратегии

Стратегия работает в 3 этапа:

### 1. Формирование диапазона (Range)
Определяется локальный диапазон цены:

- `range_high` = максимум за период
- `range_low` = минимум за период
- диапазон валиден только при достаточной волатильности

---

### 2. Пробой (Breakout)

Сигнал пробоя возникает когда:

- цена закрывается выше `range_high` → LONG setup
- цена закрывается ниже `range_low` → SHORT setup

---

### 3. Ретест (Retest confirmation)

Вход происходит только при подтверждении:

### LONG:
- цена касается уровня снизу
- затем закрывается выше уровня

### SHORT:
- цена касается уровня сверху
- затем закрывается ниже уровня

---

## 📐 Риск-менеджмент

### Stop Loss:
```text
LONG:  breakout_level - ATR * 0.5
SHORT: breakout_level + ATR * 0.5
````

### Take Profit:

```text
TP = entry ± (risk * RR)
```

Где:

* RR задаётся в `settings.RR`

---

## 📊 Индикаторы

### ATR (Average True Range)

Используется для:

* фильтра волатильности
* расчёта стопов
* фильтра ложных диапазонов

```text
TR = max(
    high - low,
    |high - prev_close|,
    |low - prev_close|
)

ATR = SMA(TR, period)
```

---

## 🧠 Состояние стратегии (State Machine)

Система хранит состояние:

```python
self.range_high
self.range_low
self.range_active
self.range_created_time

self.breakout_state  # None / "long" / "short"
self.breakout_level

self.last_breakout_level
self.last_signal_time
```

---

## 🔁 Жизненный цикл сигнала

1. Build range
2. Detect breakout
3. Wait retest
4. Confirm entry
5. Generate signal
6. Reset state

---

## 🧹 Защита от шума

### 1. Cooldown

```text
50 минут между сигналами
```

---

### 2. Anti-repeat level filter

```python
is_same_level(level1, level2, atr * 0.2)
```

---

### 3. Range validity window

```text
range живёт ограниченное время (~200 минут)
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

    def __post_init__(self):
        self.entry = round(float(self.entry), 5)
        self.stop = round(float(self.stop), 5)
        self.tp = round(float(self.tp), 5)
```

---

## 📁 Структура проекта

```
app/
│
├── main.py                 # запуск backtest / live simulation
├── config.py              # параметры стратегии
│
├── data/
│   └── data_provider.py   # загрузка CSV
│
├── models/
│   └── signal.py          # структура сигнала
│
├── strategy/
│   └── signal_engine.py   # основная логика стратегии
│
├── storage/
│   └── logger.py          # логирование сигналов
```

---

## ⚙️ Основные параметры (settings)

Пример:

```python
RANGE_PERIOD = 20
ATR_PERIOD = 14
MIN_RANGE_ATR = 1.2
RR = 2.0
PAIR = "EUR/GBP"
```

---

## ▶️ Запуск

```bash
python3 -m app.main
```

---

## 📈 Выходные данные

Пример сигнала:

```text
Signal(
    pair='EUR/GBP',
    direction='long',
    entry=0.86758,
    stop=0.86736,
    tp=0.86791,
    timestamp=2024-01-02 11:00:00
)
```

---

## ⚠️ Ограничения текущей версии

* тестируется на одном датасете (in-sample)
* нет spread / slippage симуляции
* нет фильтра тренда (EMA / HTF bias)
* нет фильтра рыночного режима (trend vs range)
* возможен overtrading в некоторых фазах рынка

---

## 🚀 Следующие улучшения (roadmap)

### 1. Фильтр тренда

* EMA200 bias
* trade only with trend

---

### 2. Фильтр флетов

* ATR compression
* volatility regime detection

---

### 3. Backtest engine

* winrate
* profit factor
* drawdown
* equity curve

---

### 4. Realistic execution

* spread simulation
* slippage
* delayed fills

---

## 📌 Итог

Это rule-based breakout + retest trading engine с:

* state machine логикой
* ATR risk model
* структурированным входом
* защитой от повторных уровней

```