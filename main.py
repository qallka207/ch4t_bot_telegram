from logging import getLogger

from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.utils.request import Request

from ufanet_bot.ar_bot.db import init_db
from ufanet_bot.ar_bot.db import add_message
from ufanet_bot.ar_bot.db import count_messages
from ufanet_bot.ar_bot.db import list_messages

from telegram_bot.config import load_config
from telegram_bot.utils import logger_factory

config = load_config()
logger = getLogger(__name__)
debug_requests = logger_factory(logger=logger)


def main():
    logger.info('Start Bot')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token='1950490429:AAEAjM2KXsDMJ0D81dJMB6iUwhKB2FYafvM',
        request=req,
        base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    init_db()

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    # updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Stop Bot')


@debug_requests
def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'аноним'

    text = update.effective_message.text
    reply_text = f'Привет, {name}!\n\n{text}'

    # Ответить пользователю
    update.message.reply_text(
        text=reply_text,
    )

    # Записать сообщение в БД
    add_message(
        user_id=user.id,
        text=text,
        )


@debug_requests
def callback_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    callback_data = update.callback_query.data

    if callback_data == COMMAND_COUNT:
        count = count_messages(user_id=user.id)
        text = f'У вас {count} сообщений!'
    elif callback_data == COMMAND_LIST:
        messages = list_messages(user_id=user.id, limit=5)
        text = '\n\n'.join([f'#{message_id} - {message_text}' for message_id, message_text in messages])
    else:
        text = 'Произошла ошибка'

    update.effective_message.reply_text(
        text=text,
    )
def main():
    logger.info('Start ArchiveBot')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token='1950490429:AAEAjM2KXsDMJ0D81dJMB6iUwhKB2FYafvM',
        request=req,
        base_url='https://telegg.ru/orig/bot',
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    init_db()

    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    updater.start_polling()
    updater.idle()
    logger.info('Stop ArchiveBot')

if __name__ == '__main__':
    main()
