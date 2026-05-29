# KURGIN v1.11.3 Real Golden Dataset + Baseline Report

Дата: 2026-05-29T00:59:25Z

## Цель

Сделать реальный baseline по загруженным supplier-файлам, чтобы дальше менять формулу только через измеримое сравнение.

## Обработанные файлы

- `SUJAN STOCK 2026 MAY (1).xlsx`
- `SUJAN STOCK 2026 MAY.xlsx`
- `SUJAN STOCK 2026 MAY1rn.xlsx`
- `UPDATED STOCK WILSON EXP.xlsx`
- `Hearts&Arrows.xlsx`
- `wilson to trinity.-1.xlsx`

## KPI

| Metric | Value |
|---|---:|
| Total rows processed | 2569 |
| OK rows | 2282 |
| Issue rows | 287 |
| Source files | 6 |
| Real golden cases selected | 114 |
| Diameter/spread review rows | 121 |
| High score diameter review rows | 39 |
| Average Score OK | 86.748 |

## Профессиональный вывод

1. Текущая формула теперь имеет реальный baseline на supplier-файлах.
2. Golden Dataset больше не только синтетический: добавлены реальные строки из поставщиков.
3. Все будущие изменения формулы нужно прогонять через `formula_comparison`.
4. Отдельно зафиксированы случаи:
   - high score + diameter warning;
   - measurement conflicts;
   - unsupported/catolog-only/missing geometry;
   - реальные edge cases по классам Score.

## Что дальше

Следующий профессиональный этап:

```text
v1.11.4 Candidate Formula Design Brief
```

Задача — не менять формулу сразу, а подготовить короткий документ:
- какие именно слабые места baseline показал;
- какие изменения допустимы;
- какой candidate v2 будет тестироваться;
- какие критерии успеха/провала.
```

