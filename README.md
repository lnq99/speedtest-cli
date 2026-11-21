# speedtest-cli

Консольный скрипт на Python, который замеряет скорость скачивания: делает N
последовательных запросов к указанному URL (например, к тяжёлой картинке),
полностью скачивает каждый ответ и печатает средний объём, среднее время запроса
и скорость скачивания.

*A console Python script that measures download speed: it makes N sequential
requests to a given URL, fully downloads each response, and prints the total
data, the average request time, and the download speed.*

## Требования / Requirements

- Python 3.8+
- `requests` (устанавливается из `requirements.txt`)

## Установка / Install

```bash
# по желанию: виртуальное окружение / optional: virtual environment
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Запуск / Run

```bash
python speedtest.py <URL>
```

Пример / Example (публичная тяжёлая картинка / a public heavy image):

```bash
python speedtest.py https://images.unsplash.com/photo-1506744038136-46273834b3fb
```

По умолчанию делается **10** запросов. Количество можно изменить флагом `-n`:

```bash
python speedtest.py <URL> -n 5 --timeout 15
```

### Параметры / Options

| Флаг | Описание |
|------|----------|
| `url` | адрес, к которому стучаться (обязательный) |
| `-n`, `--requests` | число последовательных запросов (по умолчанию 10) |
| `--timeout` | таймаут одного запроса в секундах (по умолчанию 30) |

## Пример вывода / Example output

```
Downloading https://example.com/image.jpg 10 times...
  request 1/10: 4.25 MB in 0.431 s
  ...
  request 10/10: 4.25 MB in 0.402 s

Target:               https://example.com/image.jpg
Requests:             10
Total downloaded:     42.50 MB
Average request time: 0.431 s
Download speed:       9.86 MB/s
```

## Единицы измерения / Units

Скорость печатается в **MB/s — мегабайтах в секунду** (megabytes per second).

- 1 MB = 1 000 000 байт (десятичный мегабайт, как принято для скорости передачи
  данных; это отличается от MiB = 1 048 576 байт).
- Скорость считается как `общий объём (в MB) / общее время (в секундах)` по всем
  запросам — это суммарная пропускная способность, а не среднее по отдельным
  запросам.
- «Average request time» (среднее время запроса) печатается в **секундах**.

*Speed is reported in **MB/s** (decimal megabytes, 1 MB = 1,000,000 bytes),
computed as total MB ÷ total seconds across all requests. Average request time
is in seconds.*

## Документация / Docs

- [`docs/PLAN.md`](docs/PLAN.md) — план и проектные решения / plan & design decisions
- [`docs/RUNBOOK.md`](docs/RUNBOOK.md) — как запускать и читать результат / how to run
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — как устроен код / how the code works
- [`docs/AI_USAGE.md`](docs/AI_USAGE.md) — как использовался ИИ / how AI was used
