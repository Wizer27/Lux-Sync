from sqlalchemy import text,select
from files_models import table,metadata_obj
from files_models import connect,sync_engine


def create_table():
    metadata_obj.create_all(sync_engine)