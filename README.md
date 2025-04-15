# aviso-de-oferta

Scrapea una página web cada X minutos y te avisa por Telegram si hay algún producto con precio menor al umbral definido.

## Info
Además de definir la URL, hay que analizar la estructura del HTML de esa página para setear las class correspondientes.

- Para obtener el BOT TOKEN:
  
Hablar a BotFather en Telegram y crear un /newbot

- Para obtener el CHAT ID:
  
Crear un grupo de Telegram con el bot, enviar un mensaje y acceder a esta página en un navegador: https://api.telegram.org/bot{YourBOTToken}/getUpdates

Más info: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id
