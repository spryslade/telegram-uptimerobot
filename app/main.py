#!/usr/bin/env python3

import os
import sys

from bot.telegramUptimeBot import TelegramUptimeBot

if __name__ == '__main__':
    ENV_VARS = {
        'TELEGRAM_BOT_TOKEN': '',
        'UPTIMEROBOT_API_KEY': ''
    }

    for var in ENV_VARS:
        try:
            ENV_VARS[var] = os.environ[var]
        except KeyError:
            sys.exit(f'Error: {var} is a required environment variable')

    uptimeBot = TelegramUptimeBot(ENV_VARS['TELEGRAM_BOT_TOKEN'], ENV_VARS['UPTIMEROBOT_API_KEY'])
    uptimeBot.main()
