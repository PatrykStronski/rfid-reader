import psycpog2 as pg

dbname="rfid_logs"
dbuser="azath"
host="localhost"
password="waran138"

try:
    conn = pg.connect("dbname='"+dbname+"' user='"+dbuser+"' host='"+host+"' password='"+password+"'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id SERCIAL PRIMARY KEY,u_name VARCHAR(20), l_name VARCHAR(20), uid VARCHAR(100));")
    cur.execute("CREATE TABLE IF NOT EXISTS rfid_logs(id SERCIAL PRIMARY KEY,uid VARCHAR(100), log_time BIGINT);")
except:
    print("Error connecting to Database")

def write_message(uid,log_time):
    cur = conn.cursor()
    cur.execute("INSERT INTO rfid_logs(uid,log_time) VALUES("+uid+","+log_time+");")

def find_last_time(uid):
    cur = conn.cursor()
    cur.execute("SELECT log_time FROM rfid_logs WHERE uid=''"+uid+"'' ORDER BY log_time DESC LIMIT 1")
    return cur.fetchall()[0]

def add_user(user_name, user_lname, uid):
    cur = conn.cursor()
    cur.execute("INSERT INTO users(u_name,u_lname,uid) VALUES("+user_name+","+user_lname+","+uid+");")

def fetch_user(uid):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE uid LIKE"+uid+";")
    return cur.fetchall()[0]

def fetch_all_users():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    return cur.fetchall()
