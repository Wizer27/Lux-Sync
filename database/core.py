from sqlalchemy import text,select
from database.models import table,metadata_obj
from database.sql_i import connect,sync_engine


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
def is_user_exists(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.username).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()
            return data[0] == username if data is not None else False
        except Exception as e:
            return Exception(f"Error : {e}")       
def register(username:str,hash_psw:str) -> bool:
    if is_user_exists(username):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = table.insert().values(
                username = username,
                hash_psw = hash_psw
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            return Exception(f"Error : {e}")
def login(username:str,hash_psw:str) -> bool:
    if not is_user_exists(username):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.hash_psw).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()
            return data[0] == hash_psw if data is not None else False
        except Exception as e:
            return Exception(f"Error : {e}")
