import os
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
TOKEN = "560289646:AAFzO2loYla3rOfMPBT_1S9YihU1JYN6dBU"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
dispatcher = updater.dispatcher
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://hnuvs.herokuapp.com/" + TOKEN)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
updater.idle()