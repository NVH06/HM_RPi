import mysql.connector as database
from datetime import datetime, timedelta
import asyncio
from telegram import Bot
import time
from classes.html_identifiers import LocationId


def log_scrape(logfile, host_class, zipcodes, pre_filter_count, total_count, sale_count, rent_count, buy_price, rent_price):
    print("\n-- LOG FUNCTION INITIATED --")

    upload_date = datetime.today().strftime('%Y-%m-%d')

    # Connect to database
    print("Connecting to database ...")
    connection = database.connect(
        user=host_class.user,
        password=host_class.pwd,
        host=host_class.host,
        database=host_class.database)

    cursor = connection.cursor()

    # Write to log file
    print("Writing log file ...")
    with open(logfile, "a") as f:
        f.write("\n------------------------------")
        f.write(f"\nExecution date: {upload_date}\n")
        f.write("------------------------------\n\n")

        # Get scrape meta data
        f.write(f"Zip codes:\t\t\t{zipcodes}\n")
        f.write(f"Postings before filtering:\t{pre_filter_count}\n")
        f.write(f"Postings after filtering:\t{total_count}\n\n")

        f.write(f"For sale:\t\t\t{sale_count}\n")
        f.write(f"Median price:\t\t\t{buy_price:,} EUR\n")

        f.write(f"For rent:\t\t\t{rent_count}\n")
        f.write(f"Median price:\t\t\t{rent_price:,} EUR\n\n")

        # Get count of uploaded records per table
        record_count = dict()

        for table in host_class.tables:

            count_query = f"select count(ref) " \
                          f"from {table} " \
                          f"where insert_date = '{LocationId.insert_date}';"

            cursor.execute(count_query)
            result = cursor.fetchall()

            record_count[table] = result[0][0]
            record_count[f'{table}_pct'] = int(record_count[table]/total_count*100)

            f.write(f"{table.capitalize()} table upload:\t\t{record_count[table]}/{total_count}\t\t{record_count[f'{table}_pct']}%\n")

    # Close the connection
    connection.close()
    print("Log file complete.")


def log_tg(message, logfile, chatid, apikey):
    print("\n-- SEND LOG TG FUNCTION INITIATED --")

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


def log_timer(start_time):

    # End time
    end_time = time.time()

    # Elapsed time
    elapsed_time = end_time - start_time
    elapsed_timedelta = timedelta(seconds=elapsed_time)

    hours, remainder = divmod(elapsed_timedelta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    log_time = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    print(f"Execution time: {log_time}")

    return log_time


def start_tg(chatid, apikey):

    async def send_message():
        # Create the bot instance
        bot = Bot(token=apikey)

        # Send the text message
        await bot.send_message(chat_id=chatid, text="HM script execution started")

    # Create an event loop
    loop = asyncio.get_event_loop()

    # Run the function within the event loop
    loop.run_until_complete(send_message())
