from glob import glob
import logging
import os
from random import choice

from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

from utils import get_keyboard, get_user_emo, is_cat

def greet_user(bot, update, user_data):
	emo = get_user_emo(user_data)
	user_data['emo'] = emo
	text = 'Привет {}!'.format(emo)
	update.message.reply_text(text, reply_markup=get_keyboard())

def talk_to_me(bot, update, user_data):
	emo = get_user_emo(user_data)
	user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.username,
	 			user_data['emo'], update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", 
				 update.message.chat.username,
				 update.message.chat.id, update.message.text)
	update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_cat_picture(bot, update, user_data):
	cat_list = glob('images/cat*.jp*g')
	cat_pic = choice(cat_list)
	bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())

def change_avatar(bot, update, user_data):	
	emo = get_user_emo(user_data)	
	old_emo = emo
	if 'emo' in user_data:		
		del user_data['emo']
		emo = get_user_emo(user_data)
		while emo == old_emo:
			del user_data['emo']
			emo = get_user_emo(user_data)			
	update.message.reply_text('Ваш аватар: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

def get_contact(bot, update, user_data):
	print(update.message.contact)
	update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())

def get_location(bot, update, user_data):
	print(update.message.location)
	update.message.reply_text('Готово: {}'.format(emo), reply_markup=get_keyboard())

def check_user_photo(bot, update, user_data):
	update.message.reply_text('Идёт обработка фото')
	os.makedirs('downloads', exist_ok=True)
	photo_file = bot.getFile(update.message.photo[-1].file_id)
	filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
	photo_file.download(filename)
	if is_cat(filename):
		update.message.reply_text('Котик замечен, добавлено в библиотеку')
		new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
		os.rename(filename, new_filename)
	else:
		os.remove(filename)
		update.message.reply_text('Котика не нашлось')

def anketa_start(bot, update, user_data):
	update.message.reply_text('Укажите имя и фамилию', reply_markup=ReplyKeyboardRemove())
	return "name"

def anketa_get_name(bot, update, user_data):
	user_name = update.message.text
	if len(user_name.split(" ")) != 2:
		update.message.reply_text('Вы не ввели имя и фамилию')
		return "name"
	else:
		user_data['anketa_name'] = user_name
		reply_keyboard = [('1', '2', '3', '4', '5')]

		update.message.reply_text(
			'Пожалуйста оцените бота',
			reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
		)		
		return "rating"

def anketa_rating(bot, update, user_data):
	user_data['anketa_rating'] = update.message.text
	update.message.reply_text("""Спасибо за вашу оценку {}!
Пожалуйста напишите отзыв или /skip, что бы пропустить""".format(user_data['anketa_rating']))
	return "comment"

def anketa_comment(bot, update, user_data):
	user_data['anketa_comment'] = update.message.text
	text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Ваш комментарий:</b> {anketa_comment}""".format(**user_data)
	update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode='html')
	return ConversationHandler.END

def anketa_skip_comment(bot, update, user_data):
	text = """
<b>Фамилия Имя:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}""".format(**user_data)
	update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
	return ConversationHandler.END