class LocationTable:
    df_cols = ["Ref", "Street", "House_no", "Box", "Town", "Zip_code", "Insert_date"]

class FinancialTable:
    df_cols = ["Ref", "Trans_type", "Buy_price", "Rent_price", "Monthly_costs", "REO_name", "REO_id", "Insert_date"]
    df_cols_int_types = ["Buy_price", "Rent_price", "Monthly_costs"]

class PropertyTable:
    df_cols = ["Ref", "Creation_date", "Prop_type", "Prop_subtype", "Condition", "Area", "Bedrooms",
               "Bathrooms", "Parking_indoor", "Parking_outdoor", "Parking_closedbox",
               "EPC", "Floor", "Build_year", "Garden_area", "Terrace_area", "Cadastral_income", "Views", "Insert_date"]
    df_cols_int_types = ["Area", "Bedrooms", "Bathrooms", "Parking_indoor", "Parking_outdoor",
                         "Parking_closedbox", "Floor", "Build_year", "Garden_area", "Terrace_area",
                         "Cadastral_income", "Views"]
