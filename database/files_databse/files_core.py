from sqlalchemy import text,select
from files_models import files_table,metadata_obj
from files_sqli import sync_engine
import uuid


def create_table():
    metadata_obj.create_all(sync_engine)
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
        