# Runbook — как запускать и читать результат

## 1. Подготовка

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Запуск

```bash
python speedtest.py <URL>
```

Пример (проверенные публичные ссылки):

```bash
# 10 МБ, настраиваемый размер — самый стабильный вариант
python speedtest.py "https://speed.cloudflare.com/__down?bytes=10000000"

# случайная «тяжёлая» картинка
python speedtest.py "https://picsum.photos/2000/2000"
```

> ⚠️ URL с `?` берите в кавычки, иначе zsh/bash попытается раскрыть его как
> шаблон («no matches found»).

Советы по выбору URL:
- Берите **тяжёлый** статичный файл (картинку/архив) — чем больше объём, тем
  точнее замер.
- Прямая ссылка на файл, без редиректов на HTML-страницу.

Пример полного вывода — см. [`../examples/sample-output.txt`](../examples/sample-output.txt).

## 3. Флаги

| Флаг | По умолчанию | Назначение |
|------|--------------|------------|
| `-n`, `--requests` | 10 | число последовательных запросов |
| `--timeout` | 30 | таймаут одного запроса, секунды |

```bash
python speedtest.py <URL> -n 5 --timeout 15
python speedtest.py --help
```

## 4. Как читать вывод

```
Total downloaded:     42.50 MB     <- суммарный объём по всем запросам
Average request time: 0.431 s      <- среднее время одного запроса
Download speed:       9.86 MB/s    <- суммарный объём / суммарное время
```

Скорость — в **мегабайтах в секунду** (MB/s, 1 MB = 1 000 000 байт).

## 5. Запуск тестов

Запускать **из корня проекта** (там лежит `pyproject.toml`, который добавляет
корень в `sys.path`):

```bash
pip install -r requirements-dev.txt
pytest
```

Ожидается `7 passed`. Если видите `ModuleNotFoundError: No module named
'speedtest'` — значит `pytest` запущен не из корня проекта; перейдите в каталог
`speedtest-cli` и повторите.

## 6. Частые ошибки

| Симптом | Причина | Что делать |
|---------|---------|------------|
| `request failed: ... Name or service not known` | нет сети / опечатка в домене | проверить URL и подключение |
| `request failed: ... 404` | файл не найден | взять корректную прямую ссылку |
| `request failed: ... timed out` | медленный сервер/сеть | увеличить `--timeout` |
| `downloaded 0 bytes` | сервер вернул пустой ответ | выбрать другой URL |

При любой ошибке скрипт печатает сообщение в stderr и завершается с кодом `1`.
