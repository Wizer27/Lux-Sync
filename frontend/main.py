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


def register(username:str,hash_psw:str) -> bool:
    try:
        pass
    except Exception as e:
        raise Exception(f"Error : {e}")
