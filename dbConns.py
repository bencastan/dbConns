#!/usr/bin/python
#Script to check on the number of DB idle connections
#@TODO check for the number of idle db queries
#@TODO work out the correct value to trigger the deletes at is it > 150 I have seen the sites lock up when it gets to 300 or more
#@TODO make the script object orinetated break each section into functions that can be called as needed.
#@TODO make sure as many of the require variable are defined in an editable text file.

import psycopg2
import sys
import colorama
from colorama import Fore

db_host = 'db-01.sitesuite.net'
database = 'ss'
db_user = 'ss'
db_password = ''
interval = "'5 minutes'"
countMin = 5
countMid= 20
countMax = 30

con = None

def dbConnect():
    con = None
    try:

        con = psycopg2.connect(host=db_host, database=database, user=db_user, password = db_password)
        cur = con.cursor()
        #cur.execute('SELECT version()')
        try:
            cur.execute("SELECT count(*) from pg_stat_activity where usename = 'ss' and state = 'idle' and query_start < current_timestamp - interval '60 minutes';")
        except:
            print "I can't SELECT from pg_stat_activity"

        rows = cur.fetchall()
        #print "\nRows: \n"
        for row in rows:
            #print row[0]
            return row[0]


    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:
        if con:
            con.close()



rowCount = dbConnect()
if rowCount < countMin :
    print (Fore.GREEN + "Idle queries: " + str(rowCount))
elif rowCount >= countMid and rowCount <=countMax:
    print(Fore.YELLOW + "Idle queries: " + str(rowCount))
elif rowCount >= countMax:
    print (Fore.RED + "Idle queries: " + str(rowCount))

#query = "select count(*) from pg_stat_activity where usename = 'ss' and state = 'idle'and query_start < current_timestamp - interval interval;"

#TODO add this query in to run if the number of idel DB connections gets above a limit, probably around 1500 to 200
#delete_query = " select pg_terminate_backend(pid)
#from pg_stat_activity
#where usename = 'ss'
#and state = 'idle'
#and query_start < current_timestamp - interval '120 minutes'; "
#if query > max_limit:


