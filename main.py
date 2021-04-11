from decouple import config
from telegram.ext import CommandHandler, Updater

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DEBUG = config('DEBUG')
APP_NAME_HEROKU = config('APP_NAME_HEROKU')


def comando_digitado(update, context):
    message = f'Olá, {update.message.from_user.first_name}! 😎\n\n'

    # Lendo arquivo
    with open('lista.txt', 'r') as file:
        message += file.read()

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("comando_digitado", comando_digitado))

    if DEBUG:
        updater.start_polling()

        updater.idle()
    else:
        import os
        PORT = int(os.environ.get('PORT', 5000))

        updater.start_webhook(listen="0.0.0.0",
                              port=int(PORT),
                              url_path=TELEGRAM_TOKEN)
        updater.bot.setWebhook(f'https://{APP_NAME_HEROKU}.herokuapp.com/{TELEGRAM_TOKEN}')

        updater.idle()


if __name__ == "__main__":
    print("Pressione CTRL + C para cancelar.")
    main()
