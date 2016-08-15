#!/usr/bin/python
#Script to check on the number of DB idle connections


import psycopg2
import sys

db_host = 'db-01.sitesuite.net'
database = 'ss'
db_user = 'ss'
db_password = 'maid3fee'
interval = "'5'"
max_limit = 200

con = None

try:

    con = psycopg2.connect(host=db_host, database=database, user=db_user, password = 'maid3fee')
    cur = con.cursor()
    #cur.execute('SELECT version()')
    try:
        cur.execute("SELECT count(*) from pg_stat_activity where usename = 'ss' and state = 'idle' and query_start < current_timestamp - interval '5 minutes';")
    except:
        print "I cant SELECT from bar"

    rows = cur.fetchall()
    print "\nRows: \n"
    for row in rows:
        print row[0]
        

    #ver = cur.fetchone()
    #print ver


    #rows = cur.fetchall()
    #strRows = str(rows)
    #print len(strRows)
    #for row in rows:
    #    print "   ", row[1][1]

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:

    if con:
        con.close()


query = "select count(*) from pg_stat_activity where usename = 'ss' and state = 'idle'and query_start < current_timestamp - interval interval;"

if query > max_limit:{

}
