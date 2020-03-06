import pymysql as pms
from sqlalchemy import Column, Table, INT, FLOAT, ForeignKey
import sqlalchemy as sa

def meta() -> sa.MetaData:
    """Create db metadata."""
    meta = sa.MetaData()
    Table("users_inside", meta,
          Column("ID", INT, ForeignKey("user_registry.ID"), primary_key=True))
    Table("items_in_carts", meta,
          Column("ID", INT, ForeignKey("users_inside.ID")),
          Column("Item_ID", INT, ForeignKey("item_prices.Item_ID")))
    Table("item_prices", meta,
          Column("Item_ID", INT, primary_key=True),
          Column("Item_price", FLOAT))
    Table("user_registry", meta,
          Column("ID", INT, primary_key=True),
          Column("CREDITS", FLOAT))
    return meta

def setup() -> None:
    """Setup the dockerized database."""
    # connect to the engine
    conn_str = 'mysql+pymysql://root:storelift@localhost:3306'
    engine = sa.create_engine(conn_str)
    connection = engine.connect()

    # create the db
    connection.execute("CREATE DATABASE IF NOT EXISTS store_db")
    connection.close()

    # connect to the db
    engine = sa.create_engine(conn_str + "/store_db")

    # create tables
    metadata = meta()
    metadata.create_all(engine)

    names = engine.table_names()
    if not {"items_in_carts", "item_prices", "user_registry", "users_inside"}.issubset(names):
        raise ValueError("db initialized incorrectly: ".format(names))
    else:
        print("db initialized correctly")

if __name__ == "__main__":
    setup()
