from pathlib import Path

from decouple import config
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DEBUG = config('DEBUG')
APP_NAME_HEROKU = config('APP_NAME_HEROKU')

BASE_DIR = Path(__file__).resolve().parent.parent


def comando_digitado(update, context):
    message = f'Olá, {update.message.from_user.first_name}! 😎\n'

    # Lendo arquivo
    with open(f'{BASE_DIR}/bot/cronograma.txt', 'r') as file:
        message += file.read()

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True,
        parse_mode=ParseMode.HTML)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("comando_digitado", comando_digitado))

    if DEBUG:
        updater.start_polling()

    else:
        port = int(config('PORT'))

        updater.start_webhook(listen="0.0.0.0", port=port, url_path=TELEGRAM_TOKEN)
        updater.bot.setWebhook(f'https://{APP_NAME_HEROKU}.herokuapp.com/{TELEGRAM_TOKEN}')

    updater.idle()


if __name__ == "__main__":
    print("Bot em execução.")
    main()
