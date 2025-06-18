from config import settings

from logs import addLog
from telegram import TelegramAPI

import traceback
import functools


def exceptions_catcher(): 
    """Catches all the exceptions in functions.
    If exception is noticed, it adds a new note to a logfile 
    and sends a telegram message for user about unsuccessful request.
    """

    def container(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                event = args[0]
                user_id = event.from_user.id
            except (IndexError, AttributeError):
                user_id = None

            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                log_text = f'{e}\n\n{traceback.format_exc()}'
                addLog(level='error', text=log_text)

                if user_id:                 
                    message_text = (
                        "*❌ An unknown error occurred during the execution of your request.*\n\n"
                        "Try to repeat your request, if nothing changes, wait for a while.\n\n"
                        "*🙏 We apologize for the inconvenience.*"
                    )

                    telegram_api = TelegramAPI(settings.telegram_bot_token)
                    telegram_api.sendRequest(
                        request_method='POST',
                        api_method='sendMessage',
                        parameters={
                            'chat_id': user_id,
                            'text': message_text,
                            'parse_mode': 'Markdown',
                        },
                    )
        return wrapper
    return container
