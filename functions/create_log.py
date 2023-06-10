import mysql.connector as database
from datetime import datetime
from classes.database_info import RpiHost, RpiHostTest, LocalHost
from classes.html_identifiers import LocationId


def log(logfile, host_class, zipcodes, pre_filter_count, total_count, sale_count, rent_count, buy_price, rent_price):
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

# date_name = datetime.today().strftime("%y%m%d")
# log_file = fr"C:\Users\Nils\Documents\Projects\Housing_Market\log\hm_log.txt"
#
# log(log_file, RpiHostTest)
