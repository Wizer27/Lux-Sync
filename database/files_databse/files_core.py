from sqlalchemy import text,select
from files_models import files_table,metadata_obj
from files_sqli import sync_engine
import uuid






def create_table():
    metadata_obj.create_all(sync_engine)

def is_file_exists(file_id:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.id).where(files_table.c.id == file_id)
            res = conn.execute(stmt)
            data = res.fetchone()
            return data[0] == file_id if data is not None else False
        except Exception as e:
            return Exception(f"Error : {e}")
def create_new_user_file(username:str,file_name:str,file_data):
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.insert().values(
                id = str(uuid.uuid4()),
                owner = username,
                filename = file_name,
                data = file_data
            )
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            return Exception(f"Error : {e}")
def get_user_files(username:str):
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table).where(files_table.c.owner == username)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            return Exception(f"Error : {e}")        
def delete_user_file(file_id:str) -> bool:
    if not is_file_exists(file_id):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.update().where(files_table.c.id == file_id).values(
                owner = "",
                filename = "",
                data = None
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            return Exception(f"Error : {e}")     
def update_user_file_data(file_id:str,new_data) -> bool:
    if not is_file_exists(file_id):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.update().where(files_table.c.id == file_id).values(
                data = new_data
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            return Exception(f"Error : {e}")           