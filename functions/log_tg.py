import asyncio
from telegram import Bot
from classes.cloud_info import Telegram


def send_log_tg(message, logfile, chatid, apikey):
    print("-- SEND LOG TG FUNCTION INITIATED --")

    async def send_message_and_file():
        # Create the bot instance
        bot = Bot(token=apikey)

        # Send the text message
        await bot.send_message(chat_id=chatid, text=message)

        # Send the file
        if logfile != "":
            with open(logfile, 'rb') as file:
                await bot.send_document(chat_id=chatid, document=file)

    # Create an event loop
    loop = asyncio.get_event_loop()

    # Run the function within the event loop
    loop.run_until_complete(send_message_and_file())

    print("Sending TG notification complete.")

# api_key = Telegram.api_key
# chat_id = Telegram.chat_id
# log_file = r"C:\Users\Nils\Documents\Projects\Housing_Market\log\hm_log.txt"
# log_file2 = ""
#
# send_log_tg('Test', log_file2, Telegram.chat_id, Telegram.api_key)
