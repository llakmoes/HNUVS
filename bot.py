#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = '560289646:AAFzO2loYla3rOfMPBT_1S9YihU1JYN6dBU'
PORT = int(os.environ.get('PORT', '5000'))


def echo(bot, update):
    update.message.reply_text('Bot answer: ' + update.message.text)


updater = Updater(TOKEN)

# add handlers
updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.setWebhook("https://hnuvs.herokuapp.com/" + TOKEN)
updater.idle()