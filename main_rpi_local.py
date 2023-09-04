from functions.id_scrape import get_ids
from functions.data_scrape import get_data
from functions.mysql_insert import import_data
from functions.backup_db import database_backup
from functions.log import log_scrape, log_tg, log_timer, start_tg
# from functions.gd_upload import upload_gd
from classes.types import TransType
from classes.database_info_rpi import RpiHost, RpiHostTest
from classes.cloud_info import Telegram
from datetime import datetime
import time

zip_codes = "2870,2630,2550"
execution_date = datetime.today().strftime("%d/%m/%Y - %H:%M")

date_name = datetime.today().strftime("%y%m%d")
db_backup_file = f"/home/admin/Python_scripts/HM/db_backups/{date_name}_hm_backup.sql"
log_file = f"/home/admin/Python_scripts/HM/log/{date_name[:4]}_hm_log.txt"


if __name__ == "__main__":

    # Start
    start = time.time()
    start_tg(Telegram.chat_id, Telegram.api_key)

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
        import_data(location_table, financial_table, property_table, RpiHost)

        # BACKUP DATABASE
        database_backup(db_backup_file)

        # LOG FILE
        log_scrape(log_file, RpiHost, zip_codes, pre_filter_count, total_count, sale_count, rent_count, med_buy, med_rent)

        # UPLOAD BACKUP AND LOG FILE TO GD
        # upload_gd(db_backup_file, log_file)

        # TIMER
        execution_time = log_timer(start)

        # TELEGRAM NOTIFICATION
        tg_msg = f'HM script execution SUCCESS.\nExecution time: {execution_time}'

    except Exception as e:
        err_msg = e
        execution_time = log_timer(start)
        tg_msg = f'HM script execution FAILED.\nExecution time: {execution_time}\nError:\n{err_msg}'
        log_file = ""

    log_tg(tg_msg, log_file, Telegram.chat_id, Telegram.api_key)
