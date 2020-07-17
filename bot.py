import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import *
import mysettings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
					level=logging.INFO,
					filename='bot.log'
					)

def main():
	mybot = Updater(mysettings.API_KEY)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
	dp.add_handler(CommandHandler('change_avatar', change_avatar, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

	logging.info('Starting bot')
	mybot.start_polling()
	mybot.idle()

if __name__ == "__main__":
	main()