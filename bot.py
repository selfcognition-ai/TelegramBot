from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import mysettings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
					level=logging.INFO,
					filename='bot.log'
					)

def greet_user(bot, update, user_data):
	emo = get_user_emo(user_data)
	user_data['emo'] = emo
	text = 'Привет {}!'.format(emo)
	my_keyboard = ReplyKeyboardMarkup([['/cat', '/change_avatar']],
									  resize_keyboard=True)
	update.message.reply_text(text, reply_markup=my_keyboard)

def talk_to_me(bot, update, user_data):
	emo = get_user_emo(user_data)
	user_text = "Привет {} {}! Ты написал: {}".format(update.message.chat.username,
	 			user_data['emo'], update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", 
				 update.message.chat.username,
				 update.message.chat.id, update.message.text)
	update.message.reply_text(user_text)

def send_cat_picture(bot, update, user_data):
	cat_list = glob('images/cat*.jp*g')
	cat_pic = choice(cat_list)
	bot.send_photo(chat_id=update.message.chat_id, photo=open(cat_pic, 'rb'))

def get_user_emo(user_data):
	if 'emo' in user_data:
		return user_data['emo']
	else:
		user_data['emo'] = emojize(choice(mysettings.USER_EMOJI), use_aliases=True)
		return user_data['emo']

def change_avatar(bot, update, user_data):	
	emo = get_user_emo(user_data)	
	old_emo = emo
	if 'emo' in user_data:		
		del user_data['emo']
		emo = get_user_emo(user_data)
		while emo == old_emo:
			del user_data['emo']
			emo = get_user_emo(user_data)			
	update.message.reply_text('Ваш аватар: {}'.format(emo))
		
def main():
	mybot = Updater(mysettings.API_KEY)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
	dp.add_handler(CommandHandler('change_avatar', change_avatar, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

	logging.info('Starting bot')
	mybot.start_polling()
	mybot.idle()

main()