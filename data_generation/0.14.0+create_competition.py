from faker import Faker
import psycopg2
import logging
from random import randint
import random
import os
import time
import traceback
from datetime import date
import datetime

table = 'competition'

conn = None
for i in range(int(os.getenv("CONNECTION_ATTEMPTS"))):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        break
    except Exception as e:
        conn = None
    time.sleep(20)

cur = conn.cursor()

cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (table,))
if not cur.fetchone()[0]:
    exit(0)

cur.execute(f"select count(*) from {table}")
if int(cur.fetchone()[0]) != 0:
    exit(0)

fake = Faker()

num_records = int(os.getenv("COMPETITION_COUNT"))

for i in range(num_records):
    name = fake.text()
    city = fake.city()
    country_id = randint(1, 100)
    start_date = fake.date_between(start_date=date(1900, 1, 1))
    duration = randint(1, 30)
    end_date = start_date + datetime.timedelta(days=duration)

    sql = f"""
    INSERT INTO {table} (name, city, country_id, start_date, end_date)
    VALUES (%s, %s, {country_id}, '{start_date}', '{end_date}');
    """

    cur.execute(sql, (name, city, ))

    if i % 10000 == 0:
        conn.commit()

conn.commit()

cur.close()
conn.close()

print("0.14.0 data generated")