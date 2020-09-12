import os
import sys

ENV_VARS = {
    'TELEGRAM_BOT_TOKEN': '',
    'UPTIMEROBOT_API_KEY': ''
}

for var in ENV_VARS:
    try:
        ENV_VARS[var] = os.environ[var]
    except KeyError:
        sys.exit(f'Error: {var} is a required environment variable')