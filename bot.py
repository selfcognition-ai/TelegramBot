from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import mysettings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
					level=logging.INFO,
					filename='bot.log'
					)

def main():
	mybot = Updater(mysettings.API_KEY)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))
	logging.info('Starting bot')
	mybot.start_polling()
	mybot.idle()

def greet_user(bot, update):
	text = 'Привет, друг'
	update.message.reply_text(text)

def talk_to_me(bot, update):
	user_text = "Привет {}! Ты написал: {}".format(update.message.chat.username, update.message.text)
	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
				 update.message.chat.id, update.message.text)
	update.message.reply_text(user_text)

main()