import requests
from classes.types import PropType


def get_ids(zip_code_list, trans_type_list):
    print("-- ID SCRAPE FUNCTION INITIATED --")

    pages = 50
    ids = []
    prop_subtypes = []
    trans_types = []
    towns = []
    zip_codes = []

    print("Scraping metadata...")

    for trans_type in trans_type_list:
        for page in range(1, pages):
            URL = f"https://www.immoweb.be/nl/zoeken/huis-en-appartement/{trans_type}?countries=BE&isALifeAnnuitySale=false&isAPublicSale=false&isNewlyBuilt=false&postalCodes={zip_code_list}&page={page}&orderBy=relevance"
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/75.0.3770.142 Safari/537.36'}
            page = requests.get(URL, headers=headers)
            fulltext = page.text

            textbegin = fulltext.find("<iw-search")
            textend = fulltext.find(":results-storage=")
            text = fulltext[textbegin:textend]

            # GET ID LIST
            id_begin_text = ";id&quot;:"
            id_end_text = "&quot;cluster&quot"

            id_begin_index = [i for i in range(len(text)) if text.startswith(id_begin_text, i)]
            id_end_index = [i for i in range(len(text)) if text.startswith(id_end_text, i)]

            if len(id_begin_index) == 0:
                break

            for beginpos, endpos in zip(id_begin_index, id_end_index):
                id_num = text[beginpos + 10:endpos - 1]
                ids.append(id_num)
                trans_types.append(trans_type)

            # GET PROPERTY TYPE LIST
            type_begin_text = "subtype&quot;:&quot;"
            type_end_text = "&quot;,&quot;title&quot"

            type_begin_index = [i for i in range(len(text)) if text.startswith(type_begin_text, i)]
            type_end_index = [i for i in range(len(text)) if text.startswith(type_end_text, i)]

            if len(type_begin_index) == 0:
                break

            for beginpos, endpos in zip(type_begin_index, type_end_index):
                prop = text[beginpos + 20:endpos]
                prop_subtypes.append(prop)

            # GET REGION LIST
            region_begin_text = "locality&quot;:&quot;"
            region_end_text = "&quot;,&quot;postalCode&quot"
            zip_end_text = "&quot;,&quot;street&quot"

            region_begin_index = [i for i in range(len(text)) if text.startswith(region_begin_text, i)]
            region_end_index = [i for i in range(len(text)) if text.startswith(region_end_text, i)]
            zip_end_index = [i for i in range(len(text)) if text.startswith(zip_end_text, i)]

            if len(region_begin_index) == 0:
                break

            for beginpos, endpos, zippos in zip(region_begin_index, region_end_index, zip_end_index):
                zip_code = text[zippos - 4:zippos]
                zip_codes.append(zip_code)

                town = text[beginpos + 21:endpos].lower()
                towns.append(town)

    print(f'ZIP CODE(S): {zip_code_list}')

    pre_filter = len(ids)
    print(f'Number of postings before property type filtering: {pre_filter}')

    # FILTER OUT NON RELEVANT PROPERTY TYPES
    del_index_list = []
    for index, prop_type in enumerate(prop_subtypes):
        if prop_type not in PropType.filter:
            del_index_list.append(index)

    for index in sorted(del_index_list, reverse=True):
        del ids[index]
        del prop_subtypes[index]
        del trans_types[index]
        del towns[index]
        del zip_codes[index]

    post_filter = len(ids)
    for_sale = trans_types.count("for-sale")
    for_rent = trans_types.count("for-rent")

    print(f'Number of postings after property type filtering: {post_filter}')
    print(f'For sale: {for_sale}')
    print(f'For rent: {for_rent}')

    # OUTPUT VARIABLES
    output = dict()
    output['pre_filter'] = pre_filter
    output['post_filter'] = post_filter
    output['for_sale'] = for_sale
    output['for_rent'] = for_rent
    output['ids'] = ids
    output['prop_subtypes'] = prop_subtypes
    output['trans_types'] = trans_types
    output['zip_codes'] = zip_codes
    output['towns'] = towns

    print("Scraping metadata completed.")

    return output
