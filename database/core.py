from sqlalchemy import text,select,exc
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
            raise  Exception(f"Error : {e}")
def is_user_exists(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.username).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()
            return data[0] == username if data is not None else False
        except Exception as e:
            raise  Exception(f"Error : {e}")       
def register(username:str,hash_psw:str) -> bool:
    if is_user_exists(username):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = table.insert().values(
                username = username,
                hash_psw = hash_psw,
                sub = False
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            raise  Exception(f"Error : {e}")
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
            raise  Exception(f"Error : {e}")
def select_test():
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.username)
            res = conn.execute(stmt)
            data = res.fetchall()
            return data
        except Exception as e:
            raise Exception(f"Error : {e}")

def sub(username:str) -> bool:
    if not is_user_exists(username):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = table.update().where(table.c.username == username).values(
                sub = True
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError(f"Error while executing")       
        
def is_user_subbed(username:str) -> bool:
    if not is_user_exists(username):
        raise NameError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.sub).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.scalar_one_or_none()
            if data is not None:
                return data
            return False
        except exc.SQLAlchemyError:
            raise exc.SQLAlchemyError("Error while executing")