import asyncio
from telegram import Bot


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
