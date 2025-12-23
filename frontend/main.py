import requests
import hmac
import json
import time
import hashlib
from dotenv import load_dotenv
import os


load_dotenv()
API_BASE = "http://0.0.0.0:8080"

def generate_siganture(data:dict) -> str:
    KEY = os.getenv("SIGNATURE")
    data_to_ver = data.copy()
    data_to_ver.pop("signature",None)
    data_str = json.dumps(data_to_ver, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    return str(expected_signature)

def encode_passwrod(password:str) -> str:
    data = password.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def register(username:str,hash_psw:str) -> bool:
    try:
        url = f"{API_BASE}/register"
        data = {
            "username":username,
            "hash_psw":encode_passwrod(hash_psw)
        }
        headers = {
            "X-Signature":generate_siganture(data),
            "X-Timestamp":str(int(time.time()))
        }
        resp = requests.post(url,json = data,headers=headers)
        return resp.status_code == 200
    except Exception as e:
        raise Exception(f"Error : {e}")
print(register("user2","1234"))    
    