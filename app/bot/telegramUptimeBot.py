#!/usr/bin/env python3

import datetime
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from .uptimeRobot import UptimeRobot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class TelegramUptimeBot:
    def __init__(self, telegram_bot_token: str, uptimerobot_api_key: str):
        self.telegram_bot_token = telegram_bot_token
        self.uptimeRobot: UptimeRobot = UptimeRobot(uptimerobot_api_key)

    def start(self, update: Update, context: CallbackContext):
        """Send a message when the command /start is issued."""
        update.message.reply_text('I hath been activated milord!')

    def help_command(self, update: Update, context: CallbackContext):
        """Send a message when the command /help is issued."""
        update.message.reply_text('''
        Available commands:
        /start - to start bot dialog (not required)
        /status - returns statuses of UptimeRobot monitors
        /help - returns this dialog
        ''')

    def status_command(self, update: Update, context: CallbackContext):
        """Send monitor statues when /status is issued"""
        msg = ''
        monitors = self.uptimeRobot.get_monitors()
        for monitor in monitors:
            latest_log = monitor.logs[0]
            msg = msg + f'{monitor.friendly_name} ({monitor.url}) has been {monitor.status} ' \
                        f'({latest_log.status_code} - {latest_log.status_reason}) for ' \
                        f'{str(datetime.timedelta(seconds=latest_log.duration))} since ' \
                        f'{datetime.datetime.fromtimestamp(latest_log.datetime).strftime("%c")}\n'

        update.message.reply_text(msg)

    def main(self):
        """Bot main driver"""
        updater = Updater(self.telegram_bot_token, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('help', self.help_command))
        dp.add_handler(CommandHandler('status', self.status_command))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
