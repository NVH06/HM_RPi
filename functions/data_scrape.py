import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime
from classes.types import TransType, PropType
from classes.tables import LocationTable, FinancialTable, PropertyTable
from classes.html_identifiers import LocationId, FinancialId, PropertyId

def get_data(refs, zip_codes, regions, trans_types, prop_subtypes):
    print("\n-- DATA SCRAPING FUNCTION INITIATED --")

    # LOCATION TABLE COLS LISTS
    streets = []
    house_nos = []
    house_boxs = []
    loc_insert_dates = []

    # FINANCIAL TABLE COLS LISTS
    dates = []
    buy_prices = []
    rent_prices = []
    monthly_costs = []
    reo_names = []
    reo_ids = []
    fin_insert_dates = []

    # PROPERTY TABLE COLS LISTS
    creation_dates = []
    prop_types = []
    conditions = []
    areas = []
    bedrooms = []
    bathrooms = []
    parkings_indoor = []
    parkings_outdoor = []
    parkings_closedbox = []
    epcs = []
    floors = []
    construction_years = []
    garden_areas = []
    terrace_areas = []
    cadastral_incomes = []
    views = []
    prop_insert_dates = []

    # SCRAPE DATA
    print("Scraping data...")
    for prop_subtype, region, zip_code, ref in zip(prop_subtypes, regions, zip_codes, refs):
        URL = f"https://www.immoweb.be/nl/zoekertje/{ref}"
        page = requests.get(URL)
        fulltext = page.text

        data_textbegin = fulltext.find('"bedroomCount"')
        data_textend = fulltext.find('wasPropertyVisited')
        data_text = fulltext[data_textbegin:data_textend]

        if fulltext.find('"type":"AGENCY"') != -1:
            reo_active = "YES"
            reo_textbegin = fulltext.find('"type":"AGENCY"')
            reo_textend = fulltext.find('"contactHoursMobile"')
            reo_text = fulltext[reo_textbegin:reo_textend]
        else:
            reo_active = "NO"

        # LOCATION TABLE
        try:
            street = re.search(f'{LocationId.street}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            street = np.nan
        streets.append(street)

        try:
            house_no = re.search(f'{LocationId.house_no}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            house_no = np.nan
        house_nos.append(house_no)

        try:
            house_box = re.search(f'{LocationId.house_box}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            house_box = np.nan
        house_boxs.append(house_box)

        loc_insert_dates.append(LocationId.insert_date)

        # FINANCIAL TABLE
        # date = FinancialId.date
        # dates.append(date)

        try:
            buy_price = re.search(f'{FinancialId.buy_price}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            buy_price = np.nan
        buy_prices.append(buy_price)

        try:
            rent_price = re.search(f'{FinancialId.rent_price}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            rent_price = np.nan
        rent_prices.append(rent_price)

        try:
            monthly_cost = re.search(f'{FinancialId.monthly_cost}(.*?),', data_text).group(1).replace('"', '')
            if monthly_cost == 'null':
                monthly_cost = np.nan
        except AttributeError:
            monthly_cost = np.nan
        monthly_costs.append(monthly_cost)

        if reo_active == "YES":
            reo_name = re.search(f'{FinancialId.reo_name}(.*?),', reo_text).group(1).replace('"', '')
            reo_id = re.search(f'{FinancialId.reo_id}(.*?),', reo_text).group(1).replace('"', '')
        else:
            reo_name = np.nan
            reo_id = np.nan
        reo_names.append(reo_name)
        reo_ids.append(reo_id)

        fin_insert_dates.append(FinancialId.insert_date)

        # PROPERTY TABLE
        try:
            creation_date = re.search(f'{PropertyId.creation_date}(.*?),', data_text).group(1).replace('"', '')
            creation_date = creation_date[:creation_date.find('T')]
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d').date()
        except AttributeError:
            creation_date = np.nan
        creation_dates.append(creation_date)

        try:
            condition = re.search(f'{PropertyId.condition}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            condition = np.nan
        conditions.append(condition)

        try:
            area = re.search(f'{PropertyId.area}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            area = np.nan
        areas.append(area)

        try:
            bedroom = re.search(f'{PropertyId.bedroom}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            bedroom = np.nan
        bedrooms.append(bedroom)

        try:
            bathroom = re.search(f'{PropertyId.bathroom}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            bathroom = np.nan
        bathrooms.append(bathroom)

        try:
            parking_indoor = re.search(f'{PropertyId.parking_indoor}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            parking_indoor = np.nan
        parkings_indoor.append(parking_indoor)

        try:
            parking_outdoor = re.search(f'{PropertyId.parking_outdoor}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            parking_outdoor = np.nan
        parkings_outdoor.append(parking_outdoor)

        try:
            parking_closedbox = re.search(f'{PropertyId.parking_closedbox}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            parking_closedbox = np.nan
        parkings_closedbox.append(parking_closedbox)

        try:
            epc = re.search(f'{PropertyId.epc}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            epc = np.nan
        epcs.append(epc)

        try:
            floor = re.search(f'{PropertyId.floor}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            floor = np.nan
        floors.append(floor)

        try:
            construction_year = re.search(f'{PropertyId.construction_year}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            construction_year = np.nan
        construction_years.append(construction_year)

        try:
            garden_area = re.search(f'{PropertyId.garden_area}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            garden_area = np.nan
        garden_areas.append(garden_area)

        try:
            terrace_area = re.search(f'{PropertyId.terrace_area}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            terrace_area = np.nan
        terrace_areas.append(terrace_area)

        try:
            cadastral_income = re.search(f'{PropertyId.cadastral_income}(.*?),', data_text).group(1).replace('"', '')
        except AttributeError:
            cadastral_income = np.nan
        cadastral_incomes.append(cadastral_income)

        try:
            view = re.search(f'{PropertyId.view}(.*?),', data_text).group(1).replace('"', '')
            if view == 'null':
                view = 0
        except AttributeError:
            view = np.nan
        views.append(view)

        if prop_subtype in PropType.house:
            prop_types.append("HOUSE")
        elif prop_subtype in PropType.apartment:
            prop_types.append("APARTMENT")
        else:
            prop_types.append(np.nan)

        prop_insert_dates.append(PropertyId.insert_date)

    # DATAFRAME POPULATION
    location_vals = [refs, streets, house_nos, house_boxs, regions, zip_codes, loc_insert_dates]
    financial_vals = [refs, trans_types, buy_prices, rent_prices, monthly_costs,
                      reo_names, reo_ids, fin_insert_dates]
    property_vals = [refs, creation_dates, prop_types, prop_subtypes, conditions, areas, bedrooms,
                     bathrooms, parkings_indoor, parkings_outdoor, parkings_outdoor,
                     epcs, floors, construction_years, garden_areas, terrace_areas,
                     cadastral_incomes, views, prop_insert_dates]
    all_vals = [location_vals, financial_vals, property_vals]

    # Check length of lists
    list_len = len(refs)
    for vals in all_vals:
        for list in vals:
            if len(list) != list_len:
                print(f'!! {list} length = {len(list)} not equal to {list_len} !!')
                exit()

    # Location dataframe population
    print("Populating location dataframe...")

    location_dict = dict()
    for count, col in enumerate(LocationTable.df_cols):
        location_dict[col] = location_vals[count]

    location_df = pd.DataFrame(location_dict).replace('null', np.nan)

    # Financial dataframe population
    print("Populating financial dataframe...")

    financial_dict = dict()
    for count, col in enumerate(FinancialTable.df_cols):
        financial_dict[col] = financial_vals[count]

    financial_df = pd.DataFrame(financial_dict)

    for col in FinancialTable.df_cols_int_types:
        financial_df[col] = financial_df[col].astype(float).astype('Int64')
    
    # Property dataframe population
    print("Populating property dataframe...")

    property_dict = dict()
    for count, col in enumerate(PropertyTable.df_cols):
        property_dict[col] = property_vals[count]

    property_df = pd.DataFrame(property_dict).replace('null', np.nan)

    for col in PropertyTable.df_cols_int_types:
        property_df[col] = property_df[col].astype(float).astype('Int64')

    # PRINT INFO
    med_buy = financial_df.loc[financial_df['Insert_date'] == FinancialId.insert_date, 'Buy_price'].median()
    med_rent = financial_df.loc[financial_df['Insert_date'] == FinancialId.insert_date, 'Rent_price'].median()
    print(f'Median buy price: {med_buy} EUR')
    print(f'Median rent price: {med_rent} EUR')

    # OUTPUT DICTIONNARY
    output = dict()
    output['loc'] = location_df
    output['fin'] = financial_df
    output['prop'] = property_df
    output['loc_count'] = len(location_df[location_df['Insert_date'] == FinancialId.insert_date])
    output['fin_count'] = len(financial_df[financial_df['Insert_date'] == FinancialId.insert_date])
    output['prop_count'] = len(property_df[property_df['Insert_date'] == FinancialId.insert_date])
    output['med_buy'] = med_buy
    output['med_rent'] = med_rent

    print("Data scraping completed.")

    return output

# ref_list = ["10086263", "10146505", "10232511"]
# prop_type_list = ["HOUSE", "HOUSE", "APARTMENT"]
# town_list = ["kontich", "puurs", "Liezele"]
# zip_code_list = ["2550", "2870", "2870"]
#
# ref_list = ["10302565"]
# prop_type_list = ["HOUSE"]
# town_list = ["Liezele"]
# zip_code_list = ["2870"]
#
# loc, fin, prop = get_data(ref_list, town_list, zip_code_list, TransType.for_sale, prop_type_list)
#
# print(loc)
# print(fin)
# print(prop)
