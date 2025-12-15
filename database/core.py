from sqlalchemy import text,select
from models import table,metadata_obj
from sql_i import connect,sync_engine


def create_table():
    metadata_obj.create_all(sync_engine)

def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(table)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            return Exception(f"Error : {e}")
print(get_all_data())