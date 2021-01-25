import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

# Habilitando logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = 'seuToken'


def comando_digitado(update, context):
    try:

        message = f'Olá,{update.message.from_user.first_name} + ! 😆\n\n'

        # Lendo arquivo
        with open('lista.txt', 'r') as file:
            message += file.read()

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True)
    except Exception as e:
        print(str(e))


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    updater.dispatcher.add_handler(CommandHandler(
        'comando_digitado', comando_digitado))

    # Iniciando bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook(
        'https://seuHerokuUrl.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
