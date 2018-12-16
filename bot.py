import os
import telegram
from telegram.ext import Updater
TOKEN = "560289646:AAFzO2loYla3rOfMPBT_1S9YihU1JYN6dBU"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://hnuvs.herokuapp.com/" + TOKEN)
updater.idle()