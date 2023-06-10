from datetime import datetime
from dateutil.utils import today

class LocationId:
    street = '"street":'
    house_no = '"number":'
    house_box = '"box":'
    insert_date = datetime.date(today())

class FinancialId:
    date = datetime.date(today())
    buy_price = '{"price":'
    rent_price = '"monthlyRentalPrice":'
    monthly_cost = '"monthlyRentalCosts":'
    reo_name = '"name":'
    reo_id = '"ipiNo":'
    insert_date = datetime.date(today())

class PropertyId:
    creation_date = '{"creationDate":'
    condition = '"condition":'
    area = '"netHabitableSurface":'
    bedroom = '"bedroomCount":'
    bathroom = '"bathroomCount":'
    parking_indoor = '"parkingCountIndoor":'
    parking_outdoor = '"parkingCountOutdoor":'
    parking_closedbox = '"parkingCountClosedBox":'
    epc = '"epcScore":'
    floor = '"floor":'
    construction_year = '"constructionYear":'
    garden_area = '"gardenSurface":'
    terrace_area = '"terraceSurface":'
    cadastral_income = '"cadastralIncome":'
    view = '"viewCount":'
    insert_date = datetime.date(today())
