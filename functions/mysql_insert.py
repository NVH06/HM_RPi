from sqlalchemy import create_engine


def import_data(loc_table, fin_table, prop_table, host_class):
    print("\n-- MYSQL INSERT FUNCTION INITIATED --")

    # DATABASE INFO
    hostname = host_class.host
    dbname = host_class.database
    uname = host_class.user
    pwd = host_class.pwd

    # Create SQLAlchemy engine to connect to MySQL Database
    print("Creating connection...")

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                           .format(host=hostname, db=dbname, user=uname, pw=pwd))

    # Convert dataframe to sql table
    print("Inserting dataframes to tables...")

    loc_table.to_sql('location', engine, if_exists='append', index=False)
    fin_table.to_sql('financial', engine, if_exists='append', index=False)
    prop_table.to_sql('property', engine, if_exists='append', index=False)

    print("Mysql insert completed.")
