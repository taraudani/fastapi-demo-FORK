#!/usr/bin/env python3

import mysql.connector
from mysql.connector import Error

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "hav7tz"
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Tara!"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}

@app.get("/square/{e}")
def square(e: int):
    return {"product": e * e}

@app.get("/subtract/{f}/{g}")
def square(e: int):
    return {"sum": f - g}
    
@app.get('/genres')
def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    cur.close
    db.close

@app.get('/songs')
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.image, songs.file, genres.genre FROM `songs` JOIN genres ON genres.genreid = songs.genre;;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    cur.close
    db.close
        
