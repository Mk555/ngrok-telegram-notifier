import os, logging, requests, re
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

URL_NGROK = "http://localhost:4040/api/tunnels"
TUNNEL_NAME = "ssh"

##################
## .ENV
load_dotenv()
TOKEN = os.getenv("TOKEN")
LIST_ID = os.getenv("LIST_ID").split('|')
############################

##################
## LOGS
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)
############################

##################
## NGROK
def ngrok_is_up():
    logging.info('Testing ngrok status')
    try:
        resp = requests.get(url=URL_NGROK)
        logging.info('ngrok available')
        return True
    except:
        logging.error('Can not connect to ngrok')
        return False
    return False
#
def ngrok_url():
    req_status = requests.get(url=URL_NGROK)
    tunnels = req_status.json()['tunnels']
    for tunnel in tunnels:
        logging.info(tunnel)
        if (tunnel['name'] == TUNNEL_NAME):
            tun = tunnel
    # If there is a match
    if (tun):
        url = tun['public_url']
        return url
    else:
        return '🚔 Not able to find infos about the tunnel ' + TUNNEL_NAME

############################

##################
## TELEGRAM
#### FUNCTIONS
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logging.info('Starting new conversation with ' + update.message.from_user.full_name + '\nID : ' + str(update.message.from_user.id))
    update.message.reply_text('Welcome')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    logging.info('Help asked')
    update.message.reply_text('Sorry, not available for now. You\'re fucked !')
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    logging.info('Message received : ' + update.message.text)
    update.message.reply_text(update.message.text)
def telegram_ngrok_status(update: Update, context: CallbackContext) -> None:
    logging.info('ngrok status')
    if (str(update.message.from_user.id) in LIST_ID):
        logging.info('Logging granted for : ' + str(update.message.from_user.id))
        if (ngrok_is_up()):
            logging.info('Get ngrok info')
            update.message.reply_text('☄')
            update.message.reply_text(ngrok_url())
        else:
            logging.error('🚨 🚧 ngrok not available')
    else:
        mess = '🚨 🚧 USER NOT ALLOWED : ' + str(update.message.from_user.id)
        logging.error(mess)
        update.message.reply_text(update.message.text)



##############
# Create the Updater and pass it your bot's token.
updater = Updater(token=TOKEN, use_context=True)
# Get the dispatcher to register handlers
dispatcher = updater.dispatcher
# Get the dispatcher to register handlers
dispatcher = updater.dispatcher
# Add the handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("conn", telegram_ngrok_status))
# on noncommand i.e message - echo the message on Telegram
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Start the Bot
updater.start_polling()
# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()

############################
