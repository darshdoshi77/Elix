from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri = os.environ["DATABASE_URI"]
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["USER_INFO"]
user_collections = db["users"]

def add_user_info(name:str, number:str, email: str):
    user_data = {"name": name, "number": number, "email": email}
    user_collections.insert_one(user_data)
        
def update_user_info_with_email(name:str, email: str):
    user_collections.update_one(
  {"name": name},  
  {"$set": {"email": email}}
)

def update_user_info_with_number(name:str, number:str):
    user_collections.update_one(
  {"name": name},  
  {"$set": {"number": number}}
)
    
def get_number(name:str):
    user = user_collections.find_one({"name":name})
    return user.get("number") if user else None
       
def get_email_id(name:str):
    user = user_collections.find_one({"name":name})
    return user.get("email") if user else None
    
    

def check_name_in_db(name: str)-> bool:
    return user_collections.find_one({"name":name}) is not None

