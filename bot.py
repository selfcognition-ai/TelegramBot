import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from handlers import *
import mysettings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
					level=logging.INFO,
					filename='bot.log'
					)

def main():
	mybot = Updater(mysettings.API_KEY)

	dp = mybot.dispatcher

	anketa = ConversationHandler(
		entry_points=[CommandHandler('anketa', anketa_start, pass_user_data=True)],
		states={
			"name": [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
			"rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating, pass_user_data=True)],
			"comment": [CommandHandler('skip', anketa_skip_comment, pass_user_data=True),
						MessageHandler(Filters.text, anketa_comment, pass_user_data=True)],
		},
		fallbacks=[MessageHandler(
			Filters.text | Filters.photo | Filters.video | Filters.document,
			dontknow, pass_user_data=True)]
	)
	
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(anketa)	
	dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))
	dp.add_handler(CommandHandler('change_avatar', change_avatar, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))

	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

	logging.info('Starting bot')
	mybot.start_polling()
	mybot.idle()

if __name__ == "__main__":
	main()