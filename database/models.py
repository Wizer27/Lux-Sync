from sqlalchemy import Table,Column,Integer,String,MetaData,ARRAY
from sqlalchemy.dialects.postgresql import JSONB


metadata_obj = MetaData()

table = Table("sync_app_data",
              metadata_obj,
              Column("username",String,primary_key=True),
              Column("hash_psw",String)
              )