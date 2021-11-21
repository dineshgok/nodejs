import os
import sqlite3
from flask import jsonify
from flask_api import FlaskAPI
from flask_restful import Api
from sqlalchemy import create_engine
import json
from scrape import main_scrape_func

app=FlaskAPI(__name__)
api=Api(app)
c=create_engine('sqlite:///Flask_APIproject.db')

@app.route('/', methods=['GET'])
def home():
    return json.dumps({'test': 'data'})

@app.route('/db_select_one', methods=['GET'])
def db_select_one():
    conn = c.connect()
    y = conn.execute("select * from BALLARDSPAHR_TABLE")
    return json.dumps([dict(r) for r in y])

@app.route('/db_delete', methods=['GET'])
def db_delete():
    conn = c.connect()
    trans = conn.begin()
    y = conn.execute("delete from BALLARDSPAHR_TABLE")
    trans.commit()  
    return "Deleted Successfully.."


@app.route('/create', methods=['GET'])
def create():
    try:
        conn=c.connect()
        trans=conn.begin()
        conn.execute('CREATE TABLE IF NOT EXISTS BALLARDSPAHR_TABLE(SNO INT PRIMARY KEY,SERVICE_NAME TEXT,ROLE TEXT,OFFICES TEXT,EMAILID TEXT,TELEPHONENUMBER INT,FAXNUMBER INT,PAGEURL TEXT)')
        trans.commit()
        return("User table created successfully")
    except:
        return("User table creation failed")
    finally:
        conn.close()

@app.route('/insert', methods=['GET'])
def insert():
    try:
        url = "https://www.ballardspahr.com/People"
        
        conn=c.connect()
        for data in main_scrape_func(url):
            print(data)
            trans=conn.begin()
            conn.execute('insert into BALLARDSPAHR_TABLE (SERVICE_NAME,ROLE,OFFICES,EMAILID,TELEPHONENUMBER,FAXNUMBER,PAGEURL) values '\
                    '(?,?,?,?,?,?,?)',[data['Service Name'], data['Role'], data['Offices'], data['Email'], data['Tele-Phone'], 
                                        data['Fax-Number'],data['URL']])
            trans.commit()
        return("All Data Inserted successfully")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return("User table creation failed")
    finally:
        conn.close()

app.run()