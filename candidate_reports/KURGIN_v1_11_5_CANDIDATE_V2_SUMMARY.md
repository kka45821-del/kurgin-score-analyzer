# KURGIN v1.11.5 Experimental Candidate v2 — Class Cap Only

Дата: 2026-05-29T01:21:41Z

## Что сделано

Реализован экспериментальный кандидат:

```text
formula_versions/experimental/v2_candidate/runner.py
```

Режим:

```text
class_cap_only
```

Официальная формула `current` не изменена.

## Логика

Candidate v2:

1. считает базовый результат текущей формулой;
2. смотрит diameter/spread/roundness;
3. если высокий публичный класс спорен, применяет cap;
4. не даёт плюсов за большой диаметр;
5. не штрафует грязные measurements напрямую.

## Regression metrics

| Dataset   |   Rows |   OK Rows |   Avg Delta |   Min Delta |   Max Delta |   Band Changes |   Cap Applied |
|:----------|-------:|----------:|------------:|------------:|------------:|---------------:|--------------:|
| real      |    114 |        94 |       -0.01 |       -0.94 |           0 |              1 |             1 |
| synthetic |     10 |         7 |        0    |        0    |           0 |              0 |             0 |

## Следующий шаг

Профессионально следующий этап:

```text
v1.11.6 Candidate Review Report
```

Нужно изучить конкретные строки, где:
- класс изменился;
- cap applied;
- high score + diameter issue;
- есть риск false cap.
