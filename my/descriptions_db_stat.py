import requests
import psycopg2
from bs4 import BeautifulSoup
from time import sleep



def db():
    con = psycopg2.connect(database='postgres',
                           user='postgres',
                           password='zvonarev1996',
                           host='127.0.0.1',
                           port='5432')

    cur = con.cursor()
    cur.execute("SELECT vacancies_id, description from VACANCIES ID")

    rows = cur.fetchall()
    for row in rows:
        print("vacancies id =", row[0])
        print("description =", row[1])
    #con.commit()
    con.close()



