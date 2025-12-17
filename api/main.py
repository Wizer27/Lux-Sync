from fastapi import FastAPI,Header,Depends,HTTPException,Request,status
from pydantic import Field,BaseModel
import uuid
import hmac
import hashlib
from typing import List,Optional
import uvicorn
import json
import os
from dotenv import load_dotenv
import time
from database.core import register,login
from database.files_databse.files_core import create_new_user_file,get_user_files,delete_user_file,update_user_file_data


########## SECURITY ##########
def verify_signature(data:dict,signature:str,timestamp:str) -> bool:
    if int(time.time()) - int(timestamp) > 300:
        return False
    KEY = os.getenv("SIGNATURE")
    data_to_verify = data.copy()
    data_to_verify.pop("signature",None)
    data_str = json.dumps(data_to_verify,sort_keys = True,separators = (',',':'))
    expected = hmac.new(KEY.encode(),data_str.encode(),hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature,expected)
async def safe_get(req:Request):
    api = req.headers.get("X-API-KEY")
    api_key = os.getenv("API")
    if not api or not hmac.compare_digest(api,api_key):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail = "invalid signature")


########## INIT ##########
load_dotenv()
app = FastAPI()

async def main():
    return "LUX-SYNC"

class Register(BaseModel):
    username:str
    hash_psw:str
@app.post("/register")
async def register(req:Register,x_signature:str = Header(...),x_timestamp:str = Header(...)):
    if not verify_signature(req.model_dump(),x_signature,x_timestamp):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    try:
        res = register(req.username,req.hash_psw)
        if not res:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Wrong data")
        else:
            os.makedirs(req.username,exist_ok=True)
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"Error : {e}")
@app.post("/login")
async def login(req:Register,x_signature:str = Header(...),x_timestamp:str = Header(...)):
    if not verify_signature(req.model_dump(),x_signature,x_timestamp):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    try:
        res = login(req.username,req.hash_psw)
        if not res:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Wrong data")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"Error : {e}")
class GetUserFiles(BaseModel):
    username:str    
@app.post("/get/user/files")   
async def get_user_files(req:GetUserFiles,x_signature:str = Header(...),x_timestamp:str = Header(...)):
    if not verify_signature(req.model_dump(),x_signature,x_timestamp):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,detail = "Invalid signature")
    try:
        files = get_user_files(req.username)
        return files
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = f"Error : {e}") 
    
if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0",port = 8080)    
