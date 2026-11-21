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

Пример:

```bash
python speedtest.py https://images.unsplash.com/photo-1506744038136-46273834b3fb
```

Советы по выбору URL:
- Берите **тяжёлый** статичный файл (картинку/архив) — чем больше объём, тем
  точнее замер.
- Прямая ссылка на файл, без редиректов на HTML-страницу.

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

## 5. Частые ошибки

| Симптом | Причина | Что делать |
|---------|---------|------------|
| `request failed: ... Name or service not known` | нет сети / опечатка в домене | проверить URL и подключение |
| `request failed: ... 404` | файл не найден | взять корректную прямую ссылку |
| `request failed: ... timed out` | медленный сервер/сеть | увеличить `--timeout` |
| `downloaded 0 bytes` | сервер вернул пустой ответ | выбрать другой URL |

При любой ошибке скрипт печатает сообщение в stderr и завершается с кодом `1`.
