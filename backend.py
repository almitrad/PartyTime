import sqlite3 as s3
from datetime import datetime as dtt
from datetime import datetime as dt

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

# Execute SQL scripts which create and populate tables with tester data
conn.executescript(script1)
conn.executescript(script2)

# Clears all contents from all tables
def clear_tables():
    cur.executescript(script3)

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
    + 'from invite_lst '
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
    return cur.fetchone()



"""
print(get_frat_by_code('sWq13#'))
print(get_attendees(2))
print(get_users_parties(2))

#print(get_open_parties()) # delete later

#print(get_open_parties())




dt1 = dtt.strptime(cur.fetchone()[3], '%Y-%m-%d %H:%M:%S')
dt1 = dtt.strptime(cur.fetchone()[3], '%Y-%m-%d %H:%M:%S')
print(is_now_latest(dt1))
print(dt1)
print(max(dt1,dtt.now()))

dt1 = dtt.strptime(cur.fetchone()[5], '%Y-%m-%d %H:%M:%S')
print(dt1)
print(dt1.time().hour)
print(dt1.time().hour % 12)

print(type(cur.fetchone()))
for i in cur.fetchone():
    print(i)
"""
