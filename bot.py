#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from telegram import (ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, ConversationHandler, CallbackQueryHandler)

import models
import parser
from config import Config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

pars = parser.Parser()

engine = create_engine(Config.DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

session = Session()

models.Base.metadata.create_all(engine)


def faculty(bot, update):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton(corse.group, callback_data=corse.group)] for corse in
                session.query(models.Group).filter(models.Group.faculty_id == int(query.data[-1])).all()]
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(keyboard))


def group(update, bot):
    query = update.callback_query
    group_id = session.query(models.Group).filter(models.Group.group == update.callback_query.data).first().group_id
    schedules = session.query(models.Schedule).filter(models.Schedule.date == datetime.datetime.today(),
                                                      models.Schedule.group == group_id).first()

    if schedules is None:
        schedules = pars.get_date(group_id, date=datetime.datetime.today())
        for schedule in schedules:
            text = f"{schedule.get('number')} пара {schedule.get('lesson')}['{schedule.get('lesson_type')}] " \
                f"\nНачинаеться {schedule.get('start')}\n " \
                f"Заканчиваеться {schedule.get('finish')}\n ауд. {schedule.get('lesson_room')}\n " \
                f"{schedule.get('last_name')} {schedule.get('first_name')} {schedule.get('middle_name')} "
            keyboard = [InlineKeyboardButton("Подписать", callback_data='subscribe')]
            bot.send_message(text="{}".format(text),
                             chat_id=query.message.chat_id, reply_markup=InlineKeyboardMarkup([keyboard]))
    else:
        for schedule in schedules:
            teacher = session.query(models.Teacher).query(models.Lesson).filter(
                models.Teacher.id == models.Lesson.lesson_teacher, models.Lesson.id == schedule.lesson_id).first()
            text = f"{schedule.number} пара {teacher.leson_name}['{teacher.lesson_type}] \nНачинаеться " \
                f"{schedule.start}\n Заканчиваеться {schedule.finish}\n ауд. {teacher.lesson_room}\n " \
                f"{teacher.last_name} {teacher.first_name} {teacher.middle_name} \n{schedule.date}"
            keyboard = [InlineKeyboardButton("Подписать", callback_data='subscribe')]
            bot.send_message(text="{}".format(text),
                             chat_id=query.message.chat_id, reply_markup=InlineKeyboardMarkup([keyboard]))


def start(update, bot):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.username
    facultets = [facultet.fullname for facultet in session.query(models.Faculty).filter().all()]
    keyboard = [[InlineKeyboardButton(item, callback_data=item)] for item in facultets]
    update.message.reply_text('Выберите факультет:', reply_markup=InlineKeyboardMarkup(keyboard))
    if session.query(models.User).filter(models.User.user_chat_id == chat_id).first() is None:
        try:
            user = models.User(user_chat_id=chat_id, user_name=user_name)
            session.add(user)
            session.commit()
        except Exception as er:
            logging.error(er)
            session.rollback()


def cancel(update, bot):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, errors, bot):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, errors)


def main():
    """Run bot."""
    updater = Updater(Config.TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(
        CallbackQueryHandler(faculty, pattern=r'^Факультет №\w*$|Інститут післядипломної освіти'))
    dp.add_handler(CallbackQueryHandler(group, pattern=r'^Ф\w+-\w+-\w+$'))

    dp.add_error_handler(error)

    mode = Config.MODE
    logging.info("Will run in %s mode.", mode)

    if mode == 'webhook':
        updater.start_webhook(listen="0.0.0.0", port=Config.PORT, url_path=Config.TOKEN)
        updater.bot.setWebhook("https://" + os.getenv('', 'localhost') + "/" + Config.TOKEN)
        logging.info("Listening in %s .", "https://" + Config.VIRTUAL_HOST + "/" + Config.TOKEN)
        updater.idle()
    else:
        updater.start_polling()
        logging.info("Polling...")
        updater.idle()


if __name__ == "__main__":
    main()
