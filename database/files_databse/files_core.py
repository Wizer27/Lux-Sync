from sqlalchemy import text,select,and_
from database.files_databse.files_models import files_table,metadata_obj
from database.files_databse.files_sqli import sync_engine
import uuid
from typing import List,Optional






def create_table():
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)

def is_file_exists(filename:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.filename).where(files_table.c.filename == filename)
            res = conn.execute(stmt)
            data = res.fetchone()
            return data[0] == filename if data is not None else False
        except Exception as e:
            raise  Exception(f"Error : {e}")
        
def create_new_user_file(username:str,file_name:str,file_data,size:int):
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.insert().values(
                id = str(uuid.uuid4()),
                owner = username,
                filename = file_name,
                data = file_data,
                size = size
            )
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            raise  Exception(f"Error : {e}")
        

def get_user_files(username:str) -> List:
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table).where(files_table.c.owner == username)
            res = conn.execute(stmt)
            return list(res.fetchall())
        except Exception as e:
            raise  Exception(f"Error : {e}")   


def delete_user_file(username:str,filename:str) -> bool:
    if not  is_user_has_this_file(username,filename):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.delete().where(and_(
                files_table.c.filename == filename,
                files_table.c.owner == username
            ))
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            raise  Exception(f"Error : {e}")   



def update_user_file_data(username:str,filename:str,new_data) -> bool:
    if not  is_user_has_this_file(username,filename):
        return False
    with sync_engine.connect() as conn:
        try:
            stmt = files_table.update().where(files_table.c.filename == filename).values(
                data = new_data
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            raise  Exception(f"Error : {e}")  


def get_file_data(file_name:str):
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.data).where(files_table.c.filename == file_name)
            res = conn.execute(stmt)
            return res.fetchone()
        except Exception as e:
            raise  Exception(f"Error : {e}") 


def get_user_file_names(username:str):
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.filename).where(files_table.c.owner == username)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise  Exception(f"Error : {e}")   


def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise Exception(f"Error : {e}")  
                    
def is_user_has_this_file(username:str,file_name:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.filename).where(files_table.c.owner == username)
            res = conn.execute(stmt)
            data = res.fetchall()
            if data is not None:
                return file_name in list(data)
            return False 
        except Exception as e:
            raise  Exception(f"Error : {e}")
        
def get_user_total_file_size(username:str):
    with sync_engine.connect() as conn:
        try:
            stmt = select(files_table.c.size).where(files_table.c.owner == username)
            res = conn.execute(stmt)
            data = res.fetchall()
            print(data)
        except Exception as e:
            raise Exception(f"Error : {e}")   
  