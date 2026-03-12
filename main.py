from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uuid
app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
class UserLogin(BaseModel):
 email:str
 password:str
class UserRegister(BaseModel):
 email:str
 password:str
class PortfolioItem(BaseModel):
 id:str
 title:str
 description:str
 image_url:str
class PortfolioCreate(BaseModel):
 title:str
 description:str
 image_url:str
users_db={"admin@studio.com":{"password":"admin123"}}
portfolio_db=[]
@app.get("/")
def home():return{"message":"API running"}
@app.post("/register")
def register(user:UserRegister):
 if user.email in users_db:raise HTTPException(status_code=400,detail="Email deja utilise")
 users_db[user.email]={"password":user.password}
 return{"message":"OK","email":user.email}
@app.post("/login")
def login(user:UserLogin):
 db_user=users_db.get(user.email)
 if not db_user or db_user["password"]!=user.password:raise HTTPException(status_code=401,detail="Identifiants incorrects")
 return{"message":"Login successful","email":user.email}
@app.get("/portfolio")
def get_portfolio():return portfolio_db
@app.post("/portfolio")
def add_portfolio(item:PortfolioCreate):
 new_item={"id":str(uuid.uuid4()),"title":item.title,"description":item.description,"image_url":item.image_url}
 portfolio_db.append(new_item)
 return new_item
@app.delete("/portfolio/{item_id}")
def delete_portfolio(item_id:str):
 for item in portfolio_db:
  if item["id"]==item_id:
   portfolio_db.remove(item)
   return{"message":"deleted"}
 raise HTTPException(status_code=404,detail="Not found")
