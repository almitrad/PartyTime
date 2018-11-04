import sqlite3 as s3
from datetime import datetime as dtt
from datetime import datetime as dt
from datetime import timedelta as td
import random
import string

# Create sqlite database connection and cursor
conn = s3.connect('database.db')
cur = conn.cursor()

# Read from SQL script files and store contents as string 'scripts'
file1 = open('tables.sql', "r")
script1 = file1.read()

file2 = open('insert.sql', 'r')
script2 = file2.read()

file3 = open('clear_tables.sql', 'r')
script3 = file3.read()

file_name = 'database.db'
conn = s3.connect(file_name)
cur = conn.cursor()


# Execute SQL scripts which create and populate tables with tester data
conn.executescript(script1)
conn.executescript(script2)

# Clears all contents from all tables
def clear_tables():
    cur.executescript(script3)

""" Reading from Database """

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

# Returns a list of parties that are currently going on
def get_open_parties():
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

# Return a list of users attending a party
def get_attendees(party_id):
    cur.execute('select first_name, last_name '
    + 'from user '
    + 'where user_id in( '
    + 'select user_id '
    + 'from atendee_lst '
    + 'where party_id = '
    + str(party_id) + ');')
    attendees = [row for row in cur.fetchall()]
    return attendees

# Return a list of parties a user is attending
def get_users_parties(user_id):
    cur.execute('select name '
    + 'from frat '
    + 'where frat_id in ( '
    + ' select frat_id '
    +  'from party '
    +  'where party_id in ( '
    +    'select party_id '
    +    'from atendee_lst '
    +    'where user_id = '
    + str(user_id) + '));'
    )
    parties = [row for row in cur.fetchall()]
    return parties

# Return a list of users invited to a party
def get_attendees(party_id):
    cur.execute('select first_name, last_name '
    + 'from user '
    + 'where user_id in( '
    + 'select user_id '
    + 'from invite_lst '
    + 'where party_id = '
    + str(party_id) + ');')
    attendees = [row for row in cur.fetchall()]
    return attendees

# Return a list of parties a user is invited to
def get_users_parties(user_id):
    cur.execute('select name '
    + 'from frat '
    + 'where frat_id in ( '
    + ' select frat_id '
    +  'from party '
    +  'where party_id in ( '
    +    'select party_id '
    +    'from invite_lst '
    +    'where user_id = '
    + str(user_id) + '));'
    )
    parties = [row for row in cur.fetchall()]
    return parties

# Return a frat_id corresponding to an access_code
def get_frat_by_code(access_code):
    cur.execute('select frat_id '
    + 'from frat '
    + 'where access_code = \''
    + access_code + '\';')
    result =  cur.fetchone()
    return result

def get_max_party_id():
    cur.execute('select max(party_id) from party;')
    max = cur.fetchone()
    assert max != None, 'No parties found.'
    return max[0]

def get_max_user_id():
    cur.execute('select max(user_id) from user;')
    max = cur.fetchone()
    assert max != None, 'No users found.'
    return max[0]

def get_max_frat_id():
    cur.execute('select max(frat_id) from user;')
    max = cur.fetchone()
    assert max != None, 'No frats found.'
    return max[0]

def get_max_rating_id():
    cur.execute('select max(rating_id) from rating;')
    max = cur.fetchone()
    assert max != None, 'No ratings found.'
    return max[0]


def get_frat(name):
    cur.execute('select frat_id '
    + 'from frat '
    + 'where name = \'' + name + '\';')
    result =  cur.fetchone()
    assert result != None, 'No frats found.'
    return result[0]

""" Writing to Database """
def add_user(first_name, last_name, email, passwd, gender, age, status_type='guest', frat_id=None):
    conn = s3.connect(file_name)
    cur = conn.cursor()
    user_id = get_max_user_id() + 1
    params = (str(user_id),status_type,first_name,last_name,email,passwd,gender,age,frat_id)
    cur.execute('insert into user (user_id, status_type, first_name, last_name, email, passwd, gender, age, frat_id) values ('
    + '?, ?, ?, ?, ?, ?, ?, ?, ?);', params)
    return cur.fetchone()

def add_party(frat_name, type='public', status='open', start_time=str(dtt.now() + td(days=14)), end_time=str(dtt.now() + td(days=14))):
    party_id = get_max_party_id() + 1
    frat_id = get_frat(frat_name)
    params = (str(party_id),str(frat_id),type,status,str(dtt.now()),start_time,end_time)
    cur.execute('insert into party (party_id, frat_id, type, status, posted_time, start_time, end_time) values ('
    + '?, ?, ?, ?, ?, ?, ?);', params)
    return cur.fetchone()

def add_frat(name, location, user_id, access_code=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))):
    frat_id = get_max_frat_id() + 1
    params = (frat_id, name,location,first_name,user_id,access_code)
    cur.execute('insert into user (frat_id, name, location, first_name, user_id, access_code) values ('
    + '?, ?, ?, ?, ?);', params)
    return cur.fetchone()

def add_rating(party_id, user_id, rating, rating_desc):
    rating_id = get_max_rating_id() + 1
    params = (rating_id, party_id, user_id, rating, rating_desc)
    cur.execute('insert into rating (rating_id, party_id, user_id, rating, rating_desc) values ('
    + '?, ?, ?, ?, ?);', params)
    return cur.fetchone()

def add_invite(party_id, user_id):
    params = (party_id, user_id)
    cur.execute('insert into invite_lst(party_id, user_id) values ('
    + '?, ?);', params)
    return cur.fetchone()

def add_atendee(party_id, user_id):
    params = (party_id, user_id)
    cur.execute('insert into atendee_lst(party_id, user_id) values ('
    + '?, ?);', params)
    return cur.fetchone()