from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import mysettings

def get_user_emo(user_data):
	if 'emo' in user_data:
		return user_data['emo']
	else:
		user_data['emo'] = emojize(choice(mysettings.USER_EMOJI), use_aliases=True)
		return user_data['emo']

def get_keyboard():
	contact_button = KeyboardButton('Прислать свой номер', request_contact=True)
	location_button = KeyboardButton('Прислать координаты', request_location=True)
	my_keyboard = ReplyKeyboardMarkup([
		['/cat', '/change_avatar'],
		[contact_button, location_button]
		], resize_keyboard=True)
	return my_keyboard