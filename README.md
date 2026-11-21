# speedtest-cli

Консольный скрипт на Python: делает N последовательных запросов к указанному URL
(например, к тяжёлой картинке), полностью скачивает каждый ответ и печатает общий
объём, среднее время запроса и скорость скачивания.

*A console Python script: makes N sequential requests to a URL, fully downloads
each response, and prints total data, average request time, and download speed.*

## Установка / Install

Нужен Python 3.8+.

```bash
python3 -m venv .venv && source .venv/bin/activate   # по желанию / optional
pip install -r requirements.txt
```

## Запуск / Run

```bash
# 10 МБ, настраиваемый размер / 10 MB, tunable size
python speedtest.py "https://speed.cloudflare.com/__down?bytes=10000000"

# случайная тяжёлая картинка / a random heavy image
python speedtest.py "https://picsum.photos/2000/2000"

# по умолчанию 10 запросов; меняется флагом / default 10 requests; tune with -n
python speedtest.py <URL> -n 5 --timeout 15
```

> ⚠️ URL с `?` берите в кавычки / quote URLs containing `?` (иначе zsh/bash
> раскроет его как шаблон).

Готовый пример вывода / full example run:
[`examples/sample-output.txt`](examples/sample-output.txt).

```text
$ python speedtest.py -h
usage: speedtest.py [-h] [-n COUNT] [--timeout TIMEOUT] url

Measure download speed by repeatedly downloading a URL.

positional arguments:
  url                   URL to download, e.g. a heavy image

options:
  -h, --help            show this help message and exit
  -n, --requests COUNT  number of sequential requests (default: 10)
  --timeout TIMEOUT     per-request timeout in seconds (default: 30)
```

## Единицы измерения / Units

Скорость печатается в **MB/s — мегабайтах в секунду** (megabytes per second).

- 1 MB = 1 000 000 байт (десятичный мегабайт, как принято для скорости передачи
  данных; отличается от MiB = 1 048 576 байт).
- Скорость = `общий объём (MB) / общее время (с)` по всем запросам — суммарная
  пропускная способность, а не среднее по отдельным запросам.
- «Average request time» печатается в **секундах**.

*Speed in **MB/s** (decimal, 1 MB = 1,000,000 bytes) = total MB ÷ total seconds
across all requests. Average request time is in seconds.*

## Тесты / Tests

```bash
pip install -r requirements-dev.txt
pytest        # из корня проекта / from the project root
```

Юнит-тесты чистых функций, мок-тест цикла `measure()` и герметичный
интеграционный тест против локального `http.server` — детерминированы, без
внешней сети.

## Документация / Docs

- [`docs/PLAN.md`](docs/PLAN.md) — решения / design decisions
- [`docs/RUNBOOK.md`](docs/RUNBOOK.md) — запуск и ошибки / how to run
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — устройство кода / how the code works
