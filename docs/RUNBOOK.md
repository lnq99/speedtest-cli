# Runbook — запуск и чтение результата

## 1. Подготовка

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Запуск

```bash
python speedtest.py "https://speed.cloudflare.com/__down?bytes=10000000"
python speedtest.py "https://picsum.photos/2000/2000"
python speedtest.py <URL> -n 5 --timeout 15
```

- URL с `?` берите в кавычки (иначе zsh/bash: «no matches found»).
- Берите **тяжёлый** статичный файл по прямой ссылке — чем больше объём, тем
  точнее замер.
- Полный пример вывода: [`../examples/sample-output.txt`](../examples/sample-output.txt).

Флаги: `-n/--requests` (по умолчанию 10), `--timeout` (30 с), `-h/--help`.

## 3. Как читать вывод

```
Total downloaded:     42.50 MB     <- суммарный объём
Average request time: 0.431 s      <- среднее время одного запроса
Download speed:       9.86 MB/s    <- суммарный объём / суммарное время
```

Скорость — в **MB/s** (1 MB = 1 000 000 байт).

## 4. Тесты

Запускать **из корня проекта** (там `pyproject.toml` с `pythonpath`):

```bash
pip install -r requirements-dev.txt
pytest        # ожидается: 7 passed
```

`ModuleNotFoundError: No module named 'speedtest'` → `pytest` запущен не из корня;
перейдите в каталог `speedtest-cli` и повторите.

## 5. Частые ошибки

| Симптом | Причина | Что делать |
|---------|---------|------------|
| `... Name or service not known` | нет сети / опечатка в домене | проверить URL и сеть |
| `... 404` | файл не найден | взять корректную прямую ссылку |
| `... timed out` | медленный сервер/сеть | увеличить `--timeout` |
| `downloaded 0 bytes` | пустой ответ | выбрать другой URL |

При любой ошибке — сообщение в stderr и код выхода `1`.
