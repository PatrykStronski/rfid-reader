import psycopg2 as pg
from report_creator import create_report

dbname="rfid_logs"
dbuser="postgres"
host="localhost"
password=""

try:
    conn = pg.connect("dbname='"+dbname+"' user='"+dbuser+"' host='"+host+"' password='"+password+"'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,u_name VARCHAR(20), l_name VARCHAR(20), uid VARCHAR(100));")
    cur.execute("CREATE TABLE IF NOT EXISTS card_logs(id SERIAL PRIMARY KEY,uid VARCHAR(100), log_time BIGINT);")
    conn.commit()
except:
    print("Error connecting to Database")

def write_message(uid,log_time,reader):
    cur = conn.cursor()
    cur.execute("INSERT INTO card_logs(uid,log_time,reader_id) VALUES("+uid+","+log_time+","+reader+");")
    conn.commit()

def fetch_log_times(uid):
    cur = conn.cursor()
    cur.execute("SELECT log_time FROM card_logs WHERE uid=''"+uid+"'' ORDER BY log_time")
    return cur.fetchall()

def add_user(user_name, user_lname, uid):
    cur = conn.cursor()
    cur.execute("INSERT INTO users(u_name,l_name,uid) VALUES('"+user_name+"','"+user_lname+"','"+uid+"');")
    conn.commit()

def fetch_user(uid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE uid LIKE"+uid+";")
    return cur.fetchall()[0]

def fetch_all_users():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    usrs=cur.fetchall()
    usr_json = []
    for usr in usrs:
        usr_json.append({"id": usr[0], "u_name": usr[1], "l_name": usr[2], "uid": usr[3]})
    return usr_json

def patch_user_card(id,uid):
    cur = conn.cursor()
    cur.execute("UPDATE users SET uid = '"+uid+"' WHERE id = "+id+";")
    conn.commit()

def fetch_working_times(employee_id):
    cur = conn.cursor()
    cur.execute("SELECT card_logs.uid, card_logs.log_time, card_logs.reader_id from card_logs INNER JOIN users ON users.uid LIKE card_logs.uid WHERE users.id = "+employee_id+";")
    return create_report(cur.fetchall())

def delete_user(e_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id="+e_id+";")
    conn.commit()
