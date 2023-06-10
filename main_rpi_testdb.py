from functions.id_scrape import get_ids
from functions.data_scrape import get_data
from functions.rate_scrape import get_rate
from functions.mysql_insert import import_data
from functions.backup_db import database_backup
from functions.create_log import log
from functions.log_tg import send_log_tg
from functions.gd_upload import upload_gd
from classes.types import TransType
from classes.database_info import RpiHost, RpiHostTest, LocalHost
from classes.cloud_info import Telegram
from datetime import datetime

zip_codes = "2870,2630,2550"
execution_date = datetime.today().strftime("%d/%m/%Y - %H:%M")

date_name = datetime.today().strftime("%y%m%d")
db_backup_file = fr"C:\Users\Nils\Documents\Projects\Housing_Market\hm_backup\test_hm_backup.sql"   ### change to directory path ###
log_file = fr"C:\Users\Nils\Documents\Projects\Housing_Market\log\test_hm_log.txt"   ### change to directory path ###


if __name__ == "__main__":

    try:

        # ID DATA
        meta = get_ids(zip_codes, TransType.list)

        id_list = meta['ids']
        prop_subtype_list = meta['prop_subtypes']
        trans_type_list = meta['trans_types']
        zip_code_list = meta['zip_codes']
        town_list = meta['towns']

        pre_filter_count = meta['pre_filter']
        total_count = meta['post_filter']

        sale_count = meta['for_sale']
        rent_count = meta['for_rent']

        # TABLE DATA
        scrape = get_data(id_list, zip_code_list, town_list, trans_type_list, prop_subtype_list)

        location_table = scrape['loc']
        financial_table = scrape['fin']
        property_table = scrape['prop']

        med_buy = scrape['med_buy']
        med_rent = scrape['med_rent']

        # MYSQL INSERT
        import_data(location_table, financial_table, property_table, RpiHostTest)

        # BACKUP DATABASE
        database_backup(db_backup_file)

        # LOG FILE
        log(log_file, RpiHostTest, zip_codes, pre_filter_count, total_count, sale_count, rent_count, med_buy, med_rent)

        # UPLOAD BACKUP AND LOG FILE TO GD
        upload_gd(db_backup_file, log_file)

    # TELEGRAM NOTIFICATION
        tg_msg = f'{execution_date}\nHM script execution SUCCESS.'

    except Exception as e:
        err_msg = e
        tg_msg = f'{execution_date}\nHM script execution FAILED.\nError:\n{err_msg}'
        log_file = ""

    send_log_tg(tg_msg, log_file, Telegram.chat_id, Telegram.api_key)

    # print(location_table)
    # print(financial_table)
    # print(property_table)
