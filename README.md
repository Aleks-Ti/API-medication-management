# API-medication-management

Посмотреть бота можно в Telegram `https://t.me/BaklushaBot`

В этом репозитории находится API для обработки напоминаний, и микросервис для поставки напоминаний в очередь, для отправки конечному пользователю напоминания в Telegram.

![Схема приложения](./image/architecture.png)


## ngrok

нужно для работы с веб ui миним приложение в ТГ боте

● Установка:

  curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null

  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | sudo tee /etc/apt/sources.list.d/ngrok.list

  sudo apt update && sudo apt install ngrok

  Затем зарегистрируйся на https://ngrok.com (бесплатно), возьми authtoken из дашборда и добавь:
  ngrok config add-authtoken <твой_токен>

  ---
  Что такое ngrok и зачем:

  Ngrok создаёт публичный HTTPS-туннель к твоему локальному порту. Внешний мир → ngrok серверы → твой localhost.

  Telegram → https://xxxx.ngrok-free.app → localhost:5173

  Это нужно когда сервис должен быть доступен из интернета, но ты разрабатываешь локально. В нашем случае — Telegram требует HTTPS-URL для Mini App, а твой Vite dev server работает на
  localhost.

  Основные команды:

  ngrok http 5173              # туннель на порт 5173
  ngrok http 3000              # туннель на порт 3000
  ngrok http 8001              # туннель на API
  