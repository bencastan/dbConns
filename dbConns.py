#!/usr/bin/python
#Script to check on the number of DB idle connections


import psycopg2
import sys

db_host = 'db-01.sitesuite.net'
database = 'ss'
db_user = 'ss'
db_password = ''
interval = "'5 minutes'"
max_limit = 200

con = None

try:

    con = psycopg2.connect(host=db_host, database=database, user=db_user, password = db_password)
    cur = con.cursor()
    #cur.execute('SELECT version()')
    try:
        cur.execute("SELECT count(*) from pg_stat_activity where usename = 'ss' and state = 'idle' and query_start < current_timestamp - interval '5 minutes';")
    except:
        print "I can't SELECT from pg_stat_activity"

    rows = cur.fetchall()
    print "\nRows: \n"
    for row in rows:
        print row[0]


except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:

    if con:
        con.close()





#query = "select count(*) from pg_stat_activity where usename = 'ss' and state = 'idle'and query_start < current_timestamp - interval interval;"

#TODO add this query in to run if the number of idel DB connections gets above a limit, probably around 1500 to 200
#delete_query = " select pg_terminate_backend(pid)
#from pg_stat_activity
#where usename = 'ss'
#and state = 'idle'
#and query_start < current_timestamp - interval '120 minutes'; "
#if query > max_limit:


