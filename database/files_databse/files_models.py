from sqlalchemy import Table,Column,Integer,String,MetaData,ARRAY,LargeBinary


metadata_obj = MetaData()

files_table = Table("sync_app_files",
              metadata_obj,
              Column("id",String,primary_key=True),
              Column("owner",String),
              Column("filename",String),
              Column("data",LargeBinary),
              Column("size",Integer)
              )