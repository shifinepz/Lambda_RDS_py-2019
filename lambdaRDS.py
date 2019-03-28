
# A lambda function to interact with AWS RDS MySQL

import pymysql
import sys
import json

REGION = 'us-east-1'

rds_host  = "mysqltestdb.cjuvow47mxvr.us-east-1.rds.amazonaws.com"
name = "shifin"
password = "Boom123Inec"
db_name = "shifin"

def save_events(event):
    """
    This function fetches content from mysql RDS instance
    """
    result = []
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    with conn.cursor() as cur:
        cur.execute("""insert into authors (id, name, email) values( %s, '%s', '%s')""" % (event['id'], event['name'],event['email']))
        cur.execute("""select * from authors""")
        conn.commit()
        cur.close()
        for row in cur:
            result.append(list(row))
        print ("Data from RDS...")
        print (result)
        

def main(event, context):
    save_events(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
        


event = {
   "id": 888,
   "name": "curly",
   "email": "curly@gmail.com"
 }
context = ""
main(event, context)

