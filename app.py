from flask import Flask, request, render_template
import os
import requests
import random
#from backend import initialize, get_open_parties

import sqlite3 as s3
from datetime import datetime as dtt
from datetime import datetime as dt
from datetime import timedelta as td


app = Flask(__name__)
list_of_parties = list()


conn = s3.connect('database.db', check_same_thread=False)
cur = conn.cursor()

# Read from SQL script files and store contents as string 'scripts'
file1 = open('tables.sql', "r")
script1 = file1.read()

file2 = open('insert.sql', 'r')
script2 = file2.read()

file3 = open('clear_tables.sql', 'r')
script3 = file3.read()

# Execute SQL scripts which create and populate tables with tester data
conn.executescript(script1)
conn.executescript(script2)

def get_open_parties():
	# Create sqlite database connection and cursor
    cur = conn.cursor()

    # Compares the current time to the time passed in and returns True if the current time is later
    def is_now_between(datetime1, datetime2):
        datetime1 = dtt.strptime(datetime1, '%Y-%m-%d %H:%M:%S')
        datetime2 = dtt.strptime(datetime2, '%Y-%m-%d %H:%M:%S')
        return str(min(datetime1, dtt.now()))[:19] == str(datetime1)[:19] and str(max(datetime2, dtt.now()))[:19] == str(datetime2)[:19]

    # Takes in a date object and returns a string representation of the hour:minute 12-hr time
    def get_time(datetime):
        if type(datetime) == type(''):
            datetime = dtt.strptime(datetime, '%Y-%m-%d %H:%M:%S')
        if datetime.time().hour // 12 > 0:
            return str(datetime.time().hour % 12) + str(datetime.time())[2:5] + "PM"
        else:
            return str(datetime.time().hour) + str(datetime.time())[2:5] + "AM"


    cur.execute('select b.name, c.rating, a.type, a.posted_time, a.start_time, a.end_time from party a '
    + 'join frat b '
    + 'on (a.frat_id = b.frat_id) '
    + 'join rating c '
    + 'on (a.party_id = c.party_id);')
    open_parties = []
    for i in cur.fetchall():
        post_datetime = i[3]
        end_datetime = i[4]
        if is_now_between(post_datetime, end_datetime):
            open_parties.append(i[:3] + (get_time(i[4]),))
    return open_parties

@app.route('/new_user')
def route_new_user():
    cur = conn.cursor()

    def get_max_user_id():
        cur.execute('select max(user_id) from user;')
        max = cur.fetchone()
        assert max != None, 'No users found.'
        return max[0]

    def add_user(first_name, last_name, email, passwd, gender, age, status_type='guest', frat_id=None):
        user_id = get_max_user_id() + 1
        params = (str(user_id),status_type,first_name,last_name,email,passwd,gender,age,frat_id)
        cur.execute('insert into user (user_id, status_type, first_name, last_name, email, passwd, gender, age, frat_id) values ('
        + '?, ?, ?, ?, ?, ?, ?, ?, ?);', params)
        #print(first_name, last_name, email, passwd, gender, age, status_type, frat_id)
        #print(cur.execute('select * from user;').fetchall())
        #return cur.execute('select * from user;').fetchall()

    add_user(request.args.get('first_name', 'asdf'), request.args.get('last_name', 'asdf'), request.args.get('email', 'asdf'), request.args.get('passwd', 'asdf'),
        request.args.get('gender', 'asdf'), request.args.get('age', '17'))
    return 'User successfully added'

@app.route('/new_party/')
def route3():
    cur = conn.cursor()

    def get_max_party_id():
        cur.execute('select max(party_id) from party;')
        max = cur.fetchone()
        assert max != None, 'No parties found.'
        return max[0]

    def get_frat(name):
        cur.execute('select frat_id '
        + 'from frat '
        + 'where name = \'' + name + '\';')
        result =  cur.fetchone()
        assert result != None, 'No frats found.'
        return result[0]

    def add_party(frat_name, type='public', status='open', start_time=str(dtt.now() + td(days=14)), end_time=str(dtt.now() + td(days=14))):
        party_id = get_max_party_id() + 1
        frat_id = get_frat(frat_name)
        params = (str(party_id),str(frat_id),type,status,str(dtt.now()),start_time,end_time)
        cur.execute('insert into party (party_id, frat_id, type, status, posted_time, start_time, end_time) values ('
        + '?, ?, ?, ?, ?, ?, ?);', params)

    add_party(request.args.get('frat_name', 'frat'), type=request.args.get('type', 'public'),
        status=request.args.get('status', 'open'))

    return 'Party added!'

@app.route('/get_parties/')
def route4():
    
    return str(get_open_parties())
    #return cur.execute('select * from user;').fetchall()
    #return "<br>".join(get_open_parties())

@app.route('/get_users/')

def route5():
    cur = conn.cursor()
    # Create sqlite database connection and cursor
    def get_users():
        cur.execute('select * from user;')
        return cur.fetchall()

    return str(get_users())


if __name__ == '__main__':
    app.run(debug=True)
